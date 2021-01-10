
import re


class Parser:
    # not sure if it will be neccessary later, but nice to have
    STRING_REXP = re.compile(r'("|[^"]*)')  # currently unused
    COMMENT_REXP = re.compile(r'//.*')
    COMMENT_MULTILINE_REXP = re.compile(r'/\*.*\*/', re.MULTILINE)
    # multiline used on this so that the ^ anchor still hits with finditer
    CHUNK_NAME_REXP = re.compile(r'(^[a-zA-Z_][a-zA-Z0-9_]*(?=:))', re.MULTILINE)
    FIELD_NAME_REXP = re.compile(r'([$]*[a-zA-Z_][a-zA-Z0-9_]*)')

    def __init__(self, source):
        self.source = source

    def _strip_comments(self, source):
        # strip single line comments
        src = re.sub(self.COMMENT_REXP, '', source)

        # strip multiline comments
        src = re.sub(self.COMMENT_MULTILINE_REXP, '', src)
        return src

    def _separate_chunks(self, src):
        chunks_source = []
        chunk_matches = list(re.finditer(self.CHUNK_NAME_REXP, src))
        chunk_matches_len = len(chunk_matches)
        if chunk_matches_len < 1:
            raise Exception("At least one chunk must be defined")

        chunk_match = chunk_matches[0]
        for i in range(0, chunk_matches_len):
            slice_start = chunk_match.start()
            if i+1 >= chunk_matches_len:
                slice_end = len(src)
            else:
                next_chunk_match = chunk_matches[i+1]
                slice_end = next_chunk_match.start()
                chunk_match = next_chunk_match

            s = slice(slice_start, slice_end)
            chunks_source.append(src[s])

        return chunks_source

    def parse(self):
        # this copy will be torn up a bit
        working_src = self.source

        working_src = self._strip_comments(working_src)




