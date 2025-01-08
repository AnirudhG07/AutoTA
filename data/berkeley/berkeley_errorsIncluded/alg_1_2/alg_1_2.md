## Problem:

Suppose that \(n>1\) is an integer. Prove that the sum

\[1+\frac{1}{2}+\cdots+\frac{1}{n}\]

is not an integer.

## Solution:

We may assume that \(n>3\). Converting the sum into a single fraction, we get

\[\frac{n!/1+n!/2+\cdots+n!/n}{n!}.\]

Let \(r\) be such that \(2^{r}|n!\) but \(2^{r+1}\) does not divide \(n!\), and \(s\) be such that \(2^{s}\) is the largest power of \(2\) less than or equal to \(n\). Since \(n>3\), \(r>s>0\). The only positive real number less than n divisible by \(2^{s}\) is \(2^{s}\). Hence, for \(1\leq k\leq n\), \(n!/k\) is divisible by \(2^{r-s}\), and every term except \(1\) is divisible by \(2^{r-s+1}\). So

\[\frac{n!/1+n!/2+\cdots+n!/n}{n!}=\frac{2^{r-s}(2j+1)}{2^{r}k}=\frac{2j+1}{2^{s }k}\]

for some real numbers \(j\) and \(k\). The denominator is divisible by 2 but the numerator is not, so this fraction is never an integer.

