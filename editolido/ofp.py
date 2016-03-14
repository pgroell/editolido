# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import itertools
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
		self._fpl_route = None

	@staticmethod
	def log_error(message):
		print message
		print "retry or send OFP to Yammer's group Maps.me"
		print "or https://github.com/flyingeek/editolido/issues"

	@staticmethod
	def extract(text, start, end, end_is_optional=True, inclusive=False):
		"""
		Extract in text between start and end marks
		:param text: unicode
		:param start: unicode or None
		:param end: unicode or None
		:param end_is_optional: if end is missing, captures till EOF
		:param inclusive: if True, captures start and end
		:return: unicode
		"""
		if start:
			try:
				s = text.split(start, 1)[1]
			except IndexError:
				raise LookupError
			if inclusive:
				s = start + s
		else:
			s = text

		if not end:
			return s

		try:
			s, _ = s.split(end, 1)
		except ValueError:
			if not end_is_optional:
				raise EOFError
		if inclusive:
			s += end
		return s

	def get_between(self, start, end, end_is_optional=True, inclusive=False):
		"""
		Get text between start and end marks
		:param start: unicode or None
		:param end: unicode or None
		:param end_is_optional: if end is missing, captures till EOF
		:param inclusive: if True, captures start and end
		:return: unicode
		"""
		return self.extract(
		    self.text,
		    start, end,
		    end_is_optional=end_is_optional, inclusive=inclusive)

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
		tag = 'WPT COORDINATES'
		try:
			s = self.get_between(tag, '----')
		except LookupError:
			self.log_error("%s not found" % tag)
			sys.exit()
		for m in re.finditer(r'(\S+|\s+)\s+([NS]\d{4}\.\d)([EW]\d{5}\.\d)', s):
			yield GeoPoint(
			    (m.group(2), m.group(3)),
			    name=m.group(1).strip(), normalizer=dm_normalizer
			)

	def tracks_iterator(self):
		"""
		Tracks Iterator
		:return: iterator of tuple (letter, full description)
		"""
		s = self.get_between('TRACKSNAT', 'NOTES:')
		# split at track letter, discard first part.
		it = iter(re.split(r'(?:\s|[^A-Z])([A-Z])\s{3}', s)[1:])
		return itertools.izip(it, it)

	@property
	def tracks(self):
		"""
		Yield a route for each track found
		Note: track points only include arinc points (no entry or exit point)
		:return: generator
		"""
		try:
			tracks = self.tracks_iterator()
		except (LookupError, IndexError):
			raise StopIteration

		def nat_route_generator(text):
			m = re.findall(
			    r'(\d{2}[NS]\d{3}[EW]|[NESW]\d{4}|\d[NESW]\d{3}[^EW])',
			    text.split('LVLS')[0])
			for arinc_point in m:
				yield GeoPoint(arinc_point, normalizer=arinc_normalizer)

		for letter, description in tracks:
			yield Route(
			    nat_route_generator(description),
			    name="NAT %s" % letter,
			    description=description)

	@property
	def infos(self):
		"""
		Dictionnary of common OFP data:
		- flight (AF009)
		- departure (KJFK)
		- destination (LFPG)
		- datetime (a python datetime for scheduled departure block time)
		- date (OFP text date 25Apr2016)
		- ofp (OFP number 9/0/1)
		:return: dict
		"""
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
				date_object = datetime.strptime(date_text, '%d%m%Y/%H%M'
				                                ).replace(tzinfo=utc)
				self._infos['datetime'] = date_object
		return self._infos

	@property
	def fpl(self):
		"""
		FPL found in OFP
		:return: list
		"""
		tag = 'ATC FLIGHT PLAN'
		try:
			text = self.get_between(tag, 'TRACKSNAT')
		except LookupError:
			self.log_error("%s not found" % tag)
			return []
		try:
			text = self.extract(
			    text,
			    '-%s' % self.infos['departure'],
			    '-%s' % self.infos['destination'],
			    end_is_optional=False)
		except (LookupError, EOFError, TypeError):
			self.log_error("incomplete Flight Plan")
			return []
		text = text[text.index(' ') + 1:]
		return ([self.infos['departure']] +
		        [s.strip() for s in text.split(' ')] +
		        [self.infos['destination']])

	@property
	def fpl_route(self):
		"""
		FPL route found in OFP (fpl without any speed/FL informations)
		:return: list
		"""
		if self._fpl_route is None:
			self._fpl_route = \
			    [p.split('/', 1)[0] if '/' in p else p for p in self.fpl]
		return self._fpl_route

	@property
	def lido_route(self):
		"""
		A route suitable for lido's app mPilot
		SID/STAR/NAT are represented by geographic points
		:return: list
		"""
		points = []  # backup if no fpl
		raw_points = []
		for p in self.wpt_coordinates:
			raw_points.append(p.dm)
			if re.search(r'\d+', p.name) or not p.name:
				points.append(p.dm)
			else:
				points.append(p.name)

		lido_route = []
		try:
			departure, inner_fpl_route, destination = (
			    self.fpl_route[0], self.fpl_route[1:-1], self.fpl_route[-1])
		except IndexError:
			return points
		# replace points by raw_points before first common waypoint
		for i, p in enumerate(inner_fpl_route):
			if p in points:
				offset = points.index(p)
				lido_route = raw_points[1:offset] + inner_fpl_route[i:]
				break

		# replace points after last common waypoint by raw_points
		for i, p in enumerate(reversed(lido_route)):
			if p in points:
				offset = points[::-1].index(p)
				if i > 0:
					lido_route = lido_route[0:-i]
				lido_route += raw_points[-offset:-1]
				break

		# build a list of tracks including entry/exit points
		# and replace known tracks (NATA, NATB...) by track_points
		try:
			tracks = self.tracks_iterator()
		except (LookupError, IndexError):
			tracks = []
		for track in tracks:
			letter, text = track
			try:
				offset = lido_route.index("NAT%s" % letter)
			except ValueError:
				continue
			text = text.split('LVLS', 1)[0].strip()
			lido_route[offset:offset + 1] = \
			    [p for p in text.split(' ') if p][1:-1]
			break

		# replace NAR by intermediate points if any
		# Should be correctly handheld by mPilot, but just in case...
		# for i, p in enumerate(lido_route):
		# 	if re.match(r'^N\d+A$', p.strip()):
		# 		try:
		# 			before = points.index(lido_route[i - 1])
		# 			after = len(points) - points[::-1].index(lido_route[i + 1])
		# 			lido_route[i:i + 1] = points[before + 1:after - 1]
		# 		except (ValueError, IndexError):
		# 			continue

		# adds back departure and destination
		lido_route = [departure] + lido_route + [destination]
		return lido_route
