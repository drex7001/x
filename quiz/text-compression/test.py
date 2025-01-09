import unittest

from main import compressString

class TestCompressString(unittest.TestCase):
    def test_compress_string(self):
        self.assertEqual(compressString("AABBBCCCC"), "A2B3C4")
        self.assertEqual(compressString("AaBbCc"), "AaBbCc")
        self.assertEqual(compressString(""), "")
        self.assertEqual(compressString("ABCDEFG"), "ABCDEFG")
        self.assertEqual(compressString("AAABBA"), "A3B2A")
        self.assertEqual(compressString("A"), "A")
        self.assertEqual(compressString("AAAAAAAAAA"), "A10")

if __name__ == '__main__':
    unittest.main()