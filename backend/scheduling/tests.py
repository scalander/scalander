from django.test import TestCase

# data generator
from faker import Faker

# imports all
from .scheduling import *

# import datetime
import datetime

# covers scheduling.Block
# covers scheduling.Proposal
class DataClassesTestCase(TestCase):

    def setUp(self):
        self.block1data = {
            "start": datetime.datetime(2020, 10, 10, 3, 2, 4),
            "end": datetime.datetime(2020, 12, 10, 3, 2, 4) 
        }
        self.proposal1data = {
            "start": datetime.datetime(2020, 10, 10, 3, 2, 4),
            "end": datetime.datetime(2020, 12, 10, 3, 2, 4),
            "can": [1,2],
            "cannot": [0],
            "total_weight": 10
        }

    def tearDown(self):
        del self.block1data, self.proposal1data
    
    # we do these tests to ensure that the fields 
    # of the dataclasses used stay consistent

    def test_block_serialization(self):
        block1 = Block(**self.block1data)
        block2 = Block(start=self.block1data["start"],
                       end=self.block1data["end"])

        self.assertEqual(block1, block2)

    def test_proposal_serialization(self):
        proposal1 = Proposal(**self.proposal1data)
        proposal2 = Proposal(start=self.proposal1data["start"],
                             end=self.proposal1data["end"],
                             can=self.proposal1data["can"],
                             cannot=self.proposal1data["cannot"],
                             total_weight=self.proposal1data["total_weight"])

        self.assertEqual(proposal1, proposal2)

# covers the rest of scheduling
class SchedulingTestCase(TestCase):

    def setUp(self):
        # creates the Faker instance
        # this is a nice little utility that generates
        # dates, deadlines, ranges, etc. for us
        self.faker = Faker()
        self.faker.seed_instance(71)
 
    def test_block_in_blocks(self):

        ## part 1: generate non-intersecting dates
        # we will generate date ranges that don't intersect
        # which
        
        earlier_dates = []
        for _ in range(2):
            # append first range of dates
            earlier_dates.append(self.faker.date_between("-7d",
                                                         "-3d"))
        earlier_dates = sorted(earlier_dates)
        earlier_block = Block(start=earlier_dates[0], end=earlier_dates[1])
            
        later_dates = []
        for _ in range(2):
            # append first range of dates
            later_dates.append(self.faker.date_between("+3d",
                                                       "+7d"))
        later_dates = sorted(later_dates)
        later_block = Block(start=later_dates[0], end=later_dates[1])

        # as the dates don't intersect, we should expect that
        # the block is not in the earlier blocks
        self.assertFalse(block_in_blocks(later_block, [earlier_block]))

        ## part 2: generate exactly intersecting dates
        # white-box test to test the edge case that there
        # is one block that's exactly the size of the target block
        # this should return True because an exact commitment
        # is fine
        self.assertTrue(block_in_blocks(later_block, [later_block]))

        ## part 3: block slightly off, in each direction
        day_delta = datetime.timedelta(days=1)
        
        # slightly larger
        slightly_larger_1 = Block(start=later_dates[0]-day_delta, end=later_dates[1])
        slightly_larger_2 = Block(start=later_dates[0], end=later_dates[1]+day_delta)
        self.assertTrue(block_in_blocks(later_block, [slightly_larger_1]))
        self.assertTrue(block_in_blocks(later_block, [slightly_larger_2]))
        self.assertTrue(block_in_blocks(later_block, [slightly_larger_1,
                                                      slightly_larger_2]))
        self.assertFalse(block_in_blocks(slightly_larger_1, [later_block]))
        self.assertFalse(block_in_blocks(slightly_larger_2, [later_block]))

    
