## Problem:

Let \(A=(a*{ij})*{i,j=1}^{n}\) be a real \(n\times n\) matrix with nonnegative entries such that

\[\sum*{j=1}^{n}a*{ij}=1\qquad\qquad(1\leq i\leq n).\]

Prove that no eigenvalue of \(A\) has an absolute value greater than \(1\).

## Solution:

Let \(\lambda\) be an eigenvalue of \(A\) and \(x=(x*{1},\ldots,x*{n})^{t}\) a corresponding eigenvector. Let \(x\_{i}\) be the entry of \(x\) whose absolute value is greatest. We have

\[\lambda x*{i}=\sum*{j=1}^{n}a*{ij}x*{j}\]

so

\[|\lambda||x*{i}|\leq\sum*{j=1}^{n}a*{ij}|x*{j}|\leq|x*{j}|\sum*{j=1}^{n}a*{ij} =|x*{i}|.\]

Hence, \(|\lambda|\leq 1\).
