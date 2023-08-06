"""
``DataNbaEnhancedPbpLoader`` loads pbp data for a game and creates :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` objects for each event

Enhanced data for each event includes current players on floor, score, fouls to give and number of fouls committed by each player,
plus additional data depending on event type

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import DataNbaEnhancedPbpLoader

    pbp_loader = DataNbaEnhancedPbpLoader("0021900001", "file", "/data")
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.data_nba.pbp_loader import DataNbaPbpLoader
from pbpstats.data_loader.nba_enhanced_pbp_loader import NbaEnhancedPbpLoader
from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_factory import (
    DataNbaEnhancedPbpFactory,
)


class DataNbaEnhancedPbpLoader(DataNbaPbpLoader, NbaEnhancedPbpLoader):
    """
    Loads data.nba.com source enhanced pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `data_<game_id>.json` in the `/pbp` subdirectory.
        If not provided response data will not be saved on disk.
    :raises: :obj:`~pbpstats.resources.enhanced_pbp.start_of_period.InvalidNumberOfStartersException`:
        If all 5 players that start the period for a team can't be determined.
        You can add the correct period starters to overrides/missing_period_starters.json in your data directory to fix this.
    """

    data_provider = "data_nba"
    resource = "EnhancedPbp"
    parent_object = "Game"

    def __init__(self, game_id, source, file_directory=None):
        super().__init__(game_id, source, file_directory)

    def _make_pbp_items(self):
        factory = DataNbaEnhancedPbpFactory()
        self.items = [
            factory.get_event_class(event["etype"])(event, item["p"], self.game_id)
            for item in self.data
            for event in item["pla"]
        ]
        self._add_extra_attrs_to_all_events()
