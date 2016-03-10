# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys
from datetime import datetime, timedelta, tzinfo
from editolido.route import Route
from editolido.geopoint import GeoPoint, dm_normalizer, arinc_normalizer

MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
          'Nov', 'Dec')

ZERO = timedelta(0)


# A UTC class.
class UTC(tzinfo):
	"""UTC"""

	def utcoffset(self, dt):
		return ZERO

	def tzname(self, dt):
		return b"UTC"

	def dst(self, dt):
		return ZERO
utc = UTC()


class OFP(object):
	def __init__(self, text):
		self.text = text
		self._infos = None

	def get_between(self, start, end, end_is_optional=True, inclusive=False):
		"""
		Get text between start and end marks
		:param start: unicode or None
		:param end: unicode or None
		:param end_is_optional: if end is missing, captures till EOF
		:param inclusive: if True, captures start and end
		:return: unicode
		"""
		if start:
			try:
				s = self.text.split(start, 1)[1]
			except IndexError:
				print "%s not found" % start
				print "retry or send OFP to Yammer's group Maps.me"
				print "or https://github.com/flyingeek/editolido/issues"
				raise EOFError
			if inclusive:
				s = start + s
		else:
			s = self.text

		if not end:
			return s

		try:
			s, _ = s.split(end, 1)
		except ValueError:
			if not end_is_optional:
				print "%s not found" % end
				print "retry or send OFP to Yammer's group Maps.me"
				print "or https://github.com/flyingeek/editolido/issues"
				raise EOFError
		if inclusive:
			s += end
		return s

	@property
	def filename(self):
		# allows slash in filename by using unicode char
		safe_ofp = self.infos['ofp'].replace('/', '_')
		return "{flight} {departure}-{destination} {date} {datetime:%H:%M}z " \
		       "OFP {safe_ofp}.txt".format(safe_ofp=safe_ofp, **self.infos)

	@property
	def description(self):
		return "{flight} {departure}-{destination} {date} {datetime:%H:%M}z " \
		       "OFP {ofp}".format(**self.infos)

	@property
	def wpt_coordinates(self):
		try:
			s = self.get_between('WPT COORDINATES', '----')
		except EOFError:
			sys.exit()
		for m in re.finditer(r'(\S+|\s+)\s+([NS]\d{4}\.\d)([EW]\d{5}\.\d)', s):
			yield GeoPoint(
			    (m.group(2), m.group(3)),
			    name=m.group(1).strip(), normalizer=dm_normalizer
			)

	@property
	def tracks(self):
		try:
			s = self.get_between('TRACKSNAT', 'NOTES:', end_is_optional=True)
		except EOFError:
			raise StopIteration
		# split at track letter, discard first part.
		it = iter(re.split(r'(?:\s|[^A-Z])([A-Z])\s{3}', s)[1:])

		def nat_route_generator(text):
			m = re.findall(
			    r'(\d{2}[NS]\d{3}[EW]|[NESW]\d{4}|\d[NESW]\d{3}[^EW])',
			    text.split('LVLS')[0])
			for arinc_point in m:
				yield GeoPoint(arinc_point, normalizer=arinc_normalizer)

		for letter, description in zip(it, it):
			yield Route(
			    nat_route_generator(description),
			    name="NAT %s" % letter,
			    description=description)

	@property
	def infos(self):
		if self._infos is None:
			pattern = r'\d{4}z(?P<flight>.+)' \
			          r'(?P<departure>\S{4})/' \
			          r'(?P<destination>\S{4})\s+' \
			          r'(?P<datetime>\S+/\S{4})z.*OFP\s+' \
			          r'(?P<ofp>\S+)Main'
			m = re.search(pattern, self.text)
			if m:
				self._infos = m.groupdict()
				self._infos['flight'] = self._infos['flight'].replace(' ', '')

				s = self._infos['datetime']
				self._infos['date'] = s[:-5]
				date_text = "{0}{1:0>2}{2}".format(
				    s[0:2],
				    MONTHS.index(s[2:5]) + 1,
				    s[5:]
				)
				date_object = datetime.strptime(date_text,'%d%m%Y/%H%M'
				                                ).replace(tzinfo=utc)
				self._infos['datetime'] = date_object
		return self._infos
