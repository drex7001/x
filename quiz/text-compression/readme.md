# Text Compression Function for Messaging Application

## Problem Description

You are tasked with developing a function for a text messaging application that compresses repeated characters in a string. The goal is to reduce the size of messages by replacing consecutive repeated characters with the character followed by its count. However, if the compressed version of the string is not shorter than the original string, the function should return the original string.

### Requirements
1. The function should take a string as input and return a string as output.
2. Consecutive repeated characters should be replaced with the character followed by the number of occurrences.
3. If the compressed version is not shorter than the original string, return the original string.
4. Characters are case-sensitive (`'A'` is different from `'a'`).
5. The input string will only contain alphabetic characters (a-z, A-Z).
6. Handle edge cases such as empty strings and strings with no repeating characters.
7. Optimize the function for time complexity.

---

## Input/Output Examples

### Example 1
**Input:**  
`AABBBCCCC`  

**Output:**  
`A2B3C4`  

**Explanation:**  
The character `'A'` appears 2 times, `'B'` appears 3 times, and `'C'` appears 4 times.

---

### Example 2
**Input:**  
`AaBbCc`  

**Output:**  
`AaBbCc`  

**Explanation:**  
Compression is not performed because the compressed version (`A1a1B1b1C1c1`) is longer than the original string.

---

### Example 3
**Input:**  
`""`  

**Output:**  
`""`  

**Explanation:**  
The input string is empty, so the output is also an empty string.

---

### Example 4
**Input:**  
`ABCDEFG`  

**Output:**  
`ABCDEFG`  

**Explanation:**  
There are no repeated characters, so the original string is returned.

---

### Example 5
**Input:**  
`AAABBA`  

**Output:**  
`A3B2A`  

**Explanation:**  
The character `'A'` appears 3 times initially, followed by `'B'` appearing 2 times, and `'A'` again.

---

## Function Signature

```php
function compressString(string $input): string
