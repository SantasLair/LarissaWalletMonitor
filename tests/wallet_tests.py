import unittest
from datetime import datetime, timedelta
from backend.balance_snapshot import BalanceSnapshot
from backend.wallet import Wallet


class TestWallet(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet(wallet_id="1234", wallet_name="Test Wallet")

    def test_add_balance_snapshot(self):
        self.wallet.add_balance_snapshot(100.0)
        self.assertEqual(len(self.wallet.balance_snapshots), 1)
        self.assertEqual(self.wallet.balance_snapshots[0].balance, 100.0)

    def test_get_balance_snapshots(self):
        self.wallet.add_balance_snapshot(100.0)
        self.wallet.add_balance_snapshot(200.0)
        snapshots = self.wallet.get_balance_snapshots()
        self.assertEqual(len(snapshots), 2)
        self.assertEqual(snapshots[0].balance, 100.0)
        self.assertEqual(snapshots[1].balance, 200.0)

    def test_calculate_gain(self):
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()

        self.wallet.add_balance_snapshot(100.0)  # Old snapshot
        self.wallet.add_balance_snapshot(150.0)  # New snapshot

        gain = self.wallet.calculate_gain(start_time, end_time)
        self.assertEqual(gain, 50.0)

    def test_calculate_gain_insufficient_data(self):
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()

        gain = self.wallet.calculate_gain(start_time, end_time)
        self.assertEqual(gain, 0.0)  # No snapshots

        self.wallet.add_balance_snapshot(100.0)  # Only one snapshot
        gain = self.wallet.calculate_gain(start_time, end_time)
        self.assertEqual(gain, 0.0)

    def test_calculate_oldest_gain(self):
        self.wallet.add_balance_snapshot(100.0)  # Old snapshot
        self.wallet.add_balance_snapshot(200.0)  # New snapshot

        gain, start_time, end_time = self.wallet.calculate_oldest_gain()
        self.assertEqual(gain, 100.0)
        self.assertIsNotNone(start_time)
        self.assertIsNotNone(end_time)

    def test_calculate_oldest_gain_insufficient_data(self):
        gain, start_time, end_time = self.wallet.calculate_oldest_gain()
        self.assertIsNone(gain)
        self.assertIsNone(start_time)
        self.assertIsNone(end_time)

        self.wallet.add_balance_snapshot(100.0)  # Only one snapshot
        gain, start_time, end_time = self.wallet.calculate_oldest_gain()
        self.assertIsNone(gain)
        self.assertIsNone(start_time)
        self.assertIsNone(end_time)

if __name__ == '__main__':
    unittest.main()
