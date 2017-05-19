# Key_Analyzer
This tool is used to analyze seed/key data in the form of an excel document.</br></br>

## Prerequisites: </br><ul>
<li>python3.5</br>
<li>pandas <pre><code>sudo pip install pandas
</code></pre>
<li>xlsxwriter <pre><code>sudo pip install xlrd
</code></pre></ul></br>

## Features:</br>
Given hex seed/key pairs, this tool conducts basic analysis on the data, including</br>
<ul>
<li>DEC BIN conversion
<li>XOR, first differences, and second differences
<li>Binary differences
<li>Graphs and Charts
<li>Binary Rotations and Shifts
<li>Common Appearances</ul></br>

## Usage:</br>
Download or clone the git repository. To run this program, open the command line in the downloaded location and run </br>
<pre><code>python3 parse.py [filename]
</code></pre></br>
The excel file will then open.
