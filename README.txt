A spell checker that corrects the mispelled words and suggests words
To build this spell checker we will use Peter Norvig's big text dataset (https://norvig.com/big.txt) to build the dictionary.
It has the following parts:

1. Error Detection
2. Error Correction
3. Suggested Words

Each of the parts have been explained in detail in the presentation attached.
To run this program simple use

```python3 spell-checker.py```
Enter a mispelled word with two errors at max
Now you have the correct word and the suggested words!

------------------------------------
SAMPLE INPUT 1
------------------------------------
soll

------------------------------------
SAMPLE OUTPUT 1
------------------------------------
Best Possible Correct Word:  soul
Suggested Words:  soil sole sold sell toll roll sill doll poll 



------------------------------------
SAMPLE INPUT 2
------------------------------------
entarteinment

------------------------------------
SAMPLE OUTPUT 1
------------------------------------
Best Possible Correct Word:  soul
Suggested Words:  soil sole sold sell toll roll sill doll poll 


Sample outputs shown in sample_output.png.