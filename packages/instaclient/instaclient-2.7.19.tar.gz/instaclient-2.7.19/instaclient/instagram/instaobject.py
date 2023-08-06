import abc, json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient

class InstaBaseObject(abc.ABC):
    GRAPH_IMAGE = 'GraphImage'
    GRAPH_VIDEO = 'GraphVideo'
    GRAPH_SIDECAR = 'GraphSidecar'
    GRAPH_PROFILE = 'GraphProfile'
    GRAPH_HASHTAG = 'GraphHashtag'
    GRAPH_LOCATION = 'GraphLocation'

    GRAPH_FOLLOW = 'GraphFollowAggregatedStory'
    GRAPH_LIKE = 'GraphLikeAggregatedStory'
    GRAPTH_TAGGED = 'GraphUserTaggedStory'
    GRAPH_MENTION = 'GraphMentionStory'
    GRAPH_COMMENT = 'GraphCommentMediaStory'

    def __init__(self, client:'InstaClient', id:str, type:str, viewer:str=None):
        """
        Reppresents an abstract instagram object.

        Args:
            id (str): The ID of the object. Such ID is provided by Instagram.
            viewer (BaseProfile or str): Reppresents the user account that is viewing this content. Can be either a str (username) or a `BaseProfile` object.
            type (str): Instagram object type. Can be `GRAPTH_IMAGE`, `GRAPH_VIDEO`, `GRAPH_SIDECAR`,  `GRAPH_PROFILE`, `GRAPH_HASHTAG`
        """
        # Required
        self.client = client
        self.id = id
        self.type = type
        self.viewer = viewer
        

    def __repr__(self) -> str:
        return f'InstaBaseObject<{self.id}>'


    def __getitem__(self, item: str):
        return self.__dict__[item]


    def __eq__(self, o: object) -> bool:
        if isinstance(o, InstaBaseObject):
            if o.get_id() == self.id:
                return True
            else:
                return False
        else:
            return 
            
    
    def _update(self, o: object) -> object:
        client = self.client
        if isinstance(o, self.__class__):
            args = o.to_dict()
            for attr in vars(self):
                setattr(self, attr, args.get(attr))
            self.client = client
            return self
        return None


    @classmethod
    def de_json(cls, data: str, client: 'InstaClient'):

        if not data:
            return None

        return cls(client=client, **data)  # type: ignore[call-arg]


    def to_json(self) -> str:
        """
        Returns:
            str: Json string reppresentation of the object. Any 'client' attribute will be ignored.
        """
        return json.dumps(self.to_dict())


    def to_dict(self) -> str:
        data = dict()

        for key in iter(self.__dict__):
            if key == 'client' or key.startswith('_'):
                continue

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value
        return data


    @property
    def viewer_profile(self):
        return self.client._scrape_profile(self.viewer)
        

    def get_id(self):
        return self.id


    def get_viewer(self):
        return self.viewer


    def get_type(self):
        return self.type

