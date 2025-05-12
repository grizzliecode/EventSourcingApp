import json
import os
from typing import List, Dict, Any
from event import Event, AggregateType


EVENTS_DIR = "store"
EVENTS_FILE = "events.json"

class EventStore:

    def append(self, event: Event) -> bool:
        aggregate_id = str(event.aggregate_id)
        general_path = os.path.join(os.path.abspath(EVENTS_DIR), EVENTS_FILE)
        aggregate_dir = os.path.join(os.path.abspath(EVENTS_DIR), str(event.aggregate_type))
        os.makedirs(aggregate_dir, exist_ok=True)
        aggregate_path = os.path.join(aggregate_dir, aggregate_id + ".json")
        content = []
        version = 0
        if os.path.isfile(aggregate_path):
           with open(aggregate_path, "r") as fin:
                content.extend(json.load(fin))
                version = content[-1].get("version", 0)
        if version + 1 != event.version:
            return False
        content.append(event.to_dict())
        with open(aggregate_path, "w") as fout:
            json.dump(content, fout, indent=4)
        content = []
        if os.path.isfile(general_path):
            with open(general_path, "r") as fin:
                content.extend(json.load(fin))
        content.append(event.to_dict())
        with open(general_path, "w") as fout:
            json.dump(content, fout, indent=4)
        return True

    def get_all_events(self) -> List[Event]:
        general_path = os.path.join(os.path.abspath(EVENTS_DIR), EVENTS_FILE)
        content = []
        if os.path.isfile(general_path):
            with open(general_path, "r") as fin:
                content.extend(json.load(fin))
        return [Event.from_dict(d) for d in content]

    def get_specific_events(self, aggregate_type: AggregateType, aggregate_id : int  ) -> List[Event]:
        aggregate_id = str(aggregate_id)
        aggregate_dir = os.path.join(os.path.abspath(EVENTS_DIR), str(aggregate_type))
        os.makedirs(aggregate_dir, exist_ok=True)
        aggregate_path = os.path.join(aggregate_dir, aggregate_id + ".json")
        content = []
        if os.path.isfile(aggregate_path):
            with open(aggregate_path, "r") as fin:
                content.extend(json.load(fin))
        return [Event.from_dict(d) for d in content]

    def get_last_version(self, aggregate_type: AggregateType, aggregate_id : int ) -> int:
        aggregate_id = str(aggregate_id)
        aggregate_dir = os.path.join(os.path.abspath(EVENTS_DIR), str(aggregate_type))
        os.makedirs(aggregate_dir, exist_ok=True)
        aggregate_path = os.path.join(aggregate_dir, aggregate_id + ".json")
        content = []
        if os.path.isfile(aggregate_path):
            with open(aggregate_path, "r") as fin:
                content.extend(json.load(fin))
        if(len(content) == 0):
            return 0
        return content[-1].get("version", 0)

