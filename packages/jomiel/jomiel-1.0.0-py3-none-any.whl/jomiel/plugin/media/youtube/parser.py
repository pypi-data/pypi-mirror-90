#
# jomiel
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from json import loads
from re import match as re_match
from urllib.parse import parse_qs
from urllib.parse import urlencode

from jomiel.error import ParseError
from jomiel.hypertext import http_get
from jomiel.plugin.media.parser import PluginMediaParser

# from jomiel_kore.formatter import json_pprint


class Parser(PluginMediaParser):
    """Media metadata parser implementation for YouTube."""

    __slots__ = []

    def __init__(self, uri_components):
        """Initializes the object.

        Args:
            uri_components (dict): The input URI components

        """
        super().__init__(uri_components)
        self.parse(uri_components)

    def parse(self, uri_components):
        """Parses the relevant metadata for the media.

        Args:
            uri_components (dict): The input URI components

        Raises:
            jomiel.error.ParseError if a parsing error occurred
        """

        def parse_metadata(video_info):
            """Parse meta data from the video info."""

            def parse_player_response():
                """Check that "player_response" exists and return it.

                Returns:
                    dict: the player response parsed from json

                """
                if "player_response" not in video_info:
                    raise ParseError('"player_response" not found')
                player_response = video_info["player_response"][0]
                return loads(player_response)

            def get_of(d, keyname):
                """Return a value from the given dict.

                Args:
                    d (dict): to query from
                    keyname (str): key name to query to

                Returns:
                    the value in the dict
                """
                if keyname not in d:
                    raise ParseError("%s not found" % keyname)
                return d.get(keyname)

            def playability_check_error():
                """Check for playability error in player response."""
                playability_status = get_of(resp, "playabilityStatus")
                if playability_status["status"] == "ERROR":
                    raise ParseError(playability_status["reason"])

            def parse_video_details():
                """Parse videoDetails of player_response."""
                vd = get_of(resp, "videoDetails")

                self.media.statistics.average_rating = float(
                    get_of(vd, "averageRating"),
                )
                self.media.statistics.view_count = int(
                    get_of(vd, "viewCount"),
                )
                self.media.description = get_of(vd, "shortDescription")
                self.media.length_seconds = int(
                    get_of(vd, "lengthSeconds"),
                )
                self.media.author.channel_id = get_of(vd, "channelId")
                self.media.author.name = get_of(vd, "author")
                self.media.title = get_of(vd, "title")

                thumbs = get_of(vd, "thumbnail")["thumbnails"]
                for t in thumbs:
                    thumb = self.media.thumbnail.add()
                    thumb.width = int(t["width"])
                    thumb.height = int(t["height"])
                    thumb.uri = t["url"]

            def parse_streaming_data():
                """Parse streaming data."""

                def parse(key):
                    """parse

                    Args:
                        key (str): the key name

                    """

                    def parse_format(fmt):
                        """parse_format

                        Args:
                            fmt (dict): the format dict to parse

                        """
                        s = self.media.stream.add()

                        s.quality.profile = "{} (itag={})".format(
                            fmt["qualityLabel"]
                            if "qualityLabel" in fmt
                            else fmt["quality"],
                            fmt["itag"],
                        )

                        if "width" in fmt and "height" in fmt:
                            s.quality.width = int(fmt["width"])
                            s.quality.height = int(fmt["height"])

                        s.quality.bitrate = int(fmt["bitrate"])
                        if "contentLength" in fmt:
                            s.content_length = int(fmt["contentLength"])

                        s.mime_type = fmt["mimeType"]
                        s.uri = fmt["url"]

                    formats = sd[key]

                    for fmt in formats:
                        parse_format(fmt)

                sd = get_of(resp, "streamingData")
                parse("adaptiveFormats")
                parse("formats")

            video_info = parse_qs(video_info)
            resp = parse_player_response()
            # json_pprint(resp)
            playability_check_error()
            parse_video_details()
            parse_streaming_data()

        def video_info_uri():
            """Return the URI to query the info for the video."""

            def parse_video_id():
                """Parse video ID from the input URI (components)."""
                result = re_match(
                    r"v=([\w\-_]{11})",
                    uri_components.query,
                )
                if result:
                    self.media.identifier = result.group(1)
                else:
                    raise ParseError("unable to match video ID")

            parse_video_id()

            data = urlencode(
                {
                    "video_id": self.media.identifier,
                    "eurl": "https://youtube.googleapis.com/v/"
                    + self.media.identifier,
                },
            )
            return "https://www.youtube.com/get_video_info?" + data

        info_uri = video_info_uri()

        video_info = http_get(info_uri).text
        parse_metadata(video_info)


# vim: set ts=4 sw=4 tw=72 expandtab:
