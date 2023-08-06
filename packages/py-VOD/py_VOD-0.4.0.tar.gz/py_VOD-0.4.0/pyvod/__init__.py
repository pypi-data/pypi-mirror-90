from pyvod.utils import StreamStatus, check_stream, parse_m3u8, url2stream
from os.path import join, dirname
from json_database.utils import match_one, fuzzy_match
from tempfile import gettempdir
from json_database import JsonDatabase


class Stream:
    def __init__(self, url):
        self.url = url
        self._status = StreamStatus.UNKNOWN

    @property
    def status(self):
        return check_stream(self.url)

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url


class Media:
    def __init__(self, **kwargs):
        self.data = kwargs
        if "title" not in self.data and "name" in self.data:
            self.data["title"] = self.data.pop("name")
        self.name = str(self.data["title"]).strip()
        self._streams = self.data.get("streams") or \
                        [ self.data.get("stream") or self.data["url"]]

    @property
    def identifier(self):
        return self.data.get("identifier", self.name.replace(" ", "_").lower())

    @staticmethod
    def from_json(data):
        return Media(**data)

    def as_json(self):
        return dict(self.data)

    @property
    def streams(self):
        streams = []
        for url in self._streams:
            url = url2stream(url)
            if not url:
                continue
            streams.append(Stream(url))
        return streams

    @property
    def audio_streams(self):
        streams = []
        for url in self._streams:
            url = url2stream(url, audio_only=True)
            if not url:
                continue
            streams.append(Stream(url))
        return streams

    @property
    def alive(self):
        for s in self.streams:
            if s.status == StreamStatus.OK:
                return True
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Collection:
    def __init__(self, name="pyVOD", logo=None, db_path=None):
        self.db_path = db_path or join(gettempdir(), name + ".jsondb")
        self.name = name
        self.logo = logo or join(dirname(__file__), "res",
                                 "moviesandfilms.png")

    @property
    def m3u8(self):

        m3u8_str = "#EXTM3U pyvod\n"
        m3u8_str += "#PLAYLIST: " + self.name + "\n"
        entry_template = "#EXTINF:-1 group-title=\"{group}\" tvg-id=\"{identifier}\""
        # #EXT-X-PLAYLIST-TYPE: 	VOD or EVENT
        # #EXT-X-MEDIA: 	NAME="English", TYPE=AUDIO, GROUP-ID="audio-stereo-64", LANGUAGE="en", DEFAULT=YES, AUTOSELECT=YES, URI="english.m3u8"
        for ch in self.entries:
            try:
                group = self.name

                total = len(ch.streams)
                for idx, stream in enumerate(ch.streams):
                    stream = str(ch.streams[0])
                    if stream == "None":
                        continue
                    entry = entry_template.format(group=group,
                                                  identifier=ch.identifier)
                    if total > 1:
                        name = ch.name + " " + str(idx + 1) + "/" + str(total)
                    else:
                        name = ch.name
                    m3u8_str += entry + ", " + name + "\n" + stream + "\n"
            except Exception as e:
                print(e)

        m3u8_str += "#EXT-X-ENDLIST"
        return m3u8_str

    def dump_m3u8(self, path):
        with open(path, "w") as f:
            f.write(self.m3u8)

    def add_entry(self, data, replace=True, normalize=False, key="title"):
        if isinstance(data, Media):
            data = data.as_json()

        title = data[key]
        assert title is not None

        # normalization
        if normalize:
            for key in data:
                if isinstance(data[key], list) and key != "streams":
                    for idx, i in enumerate(data[key]):
                        if isinstance(i, str):
                            data[key][idx] = i.lower()
                elif isinstance(data[key], str):
                    data[key] = data[key].lower()

        with JsonDatabase(self.name, self.db_path) as db:

            selected, item_id = self.match_entry(data, key=key)
            if selected:
                if replace:
                    print("replacing item in database")
                    db.update_item(item_id, data)
                else:
                    print("merging items")

                    # merge fields
                    for key in data:
                        if key in selected and isinstance(selected[key], list):
                            selected[key] += data[key]
                            # remove duplicates
                            selected[key] = list(set(selected[key]))
                        else:
                            selected[key] = data[key]

                    db.update_item(item_id, selected)
                return
            db.add_item(data)

    def match_entry(self, data, key="title"):
        if isinstance(data, Media):
            data = data.as_json()
        db = JsonDatabase(self.name, self.db_path)
        # search by key/value pair
        movies = db.search_by_value(key, data[key])

        if len(movies):
            selected = movies[0]
            item_id = db.get_item_id(selected)
            if item_id >= 0:
                return selected, item_id
        return None, -1

    def replace_entry(self, data, key="title"):
        self.add_entry(data, replace=True, key=key)

    def update_entry(self, data, key="title"):
        self.add_entry(data, replace=False, key=key)

    def remove_entry(self, data, normalize=False, key="title"):
        if isinstance(data, Media):
            data = data.as_json()

        title = data.get(key)
        assert title is not None

        # normalization
        if normalize:
            for key in data:
                if isinstance(data[key], list) and key != "streams":
                    for idx, i in enumerate(data[key]):
                        if isinstance(i, str):
                            data[key][idx] = i.lower()
                elif isinstance(data[key], str):
                    data[key] = data[key].lower()

        with JsonDatabase(self.name, self.db_path) as db:

            # search by key/value pair
            movies = db.search_by_value(key, data[key])

            if len(movies):
                selected = movies[0]
                item_id = db.get_item_id(selected)
                if item_id >= 0:
                    print("Removing item from db")
                    db.remove_item(item_id)

    def print_collection(self):
        JsonDatabase(self.name, self.db_path).print()

    @property
    def entries(self):
        entries = []
        collection = JsonDatabase(self.name, self.db_path)
        for ch in collection.db[self.name]:
            if not ch.get("streams") and not ch.get("stream") and not \
                    ch.get("url"):
                continue
            entries.append(Media.from_json(ch))
        return entries

    @property
    def stream_names(self):
        return list(set([ch.name for ch in self.entries]))

    @property
    def total_entries(self):
        return len(JsonDatabase(self.name, self.db_path))

    def remove_bad_entries(self, key="title"):
        for ch in self.entries:
            if not ch.alive:
                self.remove_entry(ch, key=key)
                print(ch.name, "DEAD")

    def search(self, query, max_res=5,
               tag_whitelist=None):
        scores = []
        query = query.lower()
        words = query.split(" ")
        tag_whitelist = tag_whitelist or []
        tag_whitelist = [t.lower().strip() for t in tag_whitelist]

        def common(l1, l2):
            return list(set(l1).intersection(l2))

        for ch in self.entries:

            # check allowed tags
            if tag_whitelist:
                i = common(tag_whitelist, ch.data["tags"])
                if not len(i):
                    continue

            # fuzzy match name for base score
            score = fuzzy_match(query, ch.name)

            # partial match name
            if ch.name in query:
                score += 0.4
            elif ch.name.lower() in query.lower():
                score += 0.25

            if query in ch.name:
                score += 0.5
            elif query.lower() in ch.name.lower():
                score += 0.35

            # count word overlap with movie tags
            tags = [t.strip() for t in ch.data["tags"]]

            word_intersection = common(words, tags)
            pct = len(word_intersection) / len(words)
            score += pct

            # fuzzy match tags

            if len(tags):
                _, _score = match_one(query, tags)
                score += _score * 0.5
                for t in tags:
                    if t in query:
                        score += 0.3

            # re-scale score values
            score = score / 4

            # name match bonus
            # we really want to increase score in this case
            name = ch.name.replace("_", " ")
            word_intersection = common(words, name.split())
            pct = len(word_intersection) / len(words)
            if pct > 0:
                score += 0.4 * pct

            scores.append((ch, min(1, score)))

        scores = sorted(scores, key=lambda k: k[1], reverse=True)
        return scores[:max_res]
