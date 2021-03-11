from typing import Dict
import json

from graylog import (
    Configuration,
    Graylog, 
    GraylogBasicAuthenticator,
    GraylogAbsoluteSearch,
    TimeRange,
    GraylogExtractor, 
    GraylogQueryParser)

def _get_uniq_req_ids(p: GraylogQueryParser):
    uniq_request_ids = []
    for m in p.get_messages():
        if m['request_id'] in uniq_request_ids:
            continue
        uniq_request_ids.append(m['request_id'])
    print(f"{len(uniq_request_ids)=}")

    return " OR ".join([x.replace('-', r'\-') for x in uniq_request_ids])


def main():
    cfg = Configuration("./config.json").parse()
    env = "prod"

    auth = GraylogBasicAuthenticator(cfg.username, cfg.password)
    graylog = Graylog(api_server=cfg.server, auth=auth)
    search = GraylogAbsoluteSearch(server=graylog)
    start, end = TimeRange().ndays_before(-1)

    extractor = GraylogExtractor(search, start=start, end=end)

    _filter_prefix = f"environment:{env} AND _exists_:request_id AND pyro"
    _error_filter = f"{_filter_prefix} AND error"

    result = extractor.do_search(q=_error_filter, limit=2)
    total_errors = result.total_results
    print(f"total errors {total_errors}")

    result = extractor.do_search(q=_error_filter, limit=total_errors)

    id_filter = _get_uniq_req_ids(result)
    filter_with_request_id = f"{_filter_prefix} AND request_id:({id_filter})"
    print(f"filter={filter_with_request_id}")

    result = extractor.do_search(q=filter_with_request_id, limit=total_errors, raw=True)

    print("saving to file...")
    with open("gl.log", "w+") as fp:
        json.dump(result, fp)

if __name__ == "__main__":
    main()