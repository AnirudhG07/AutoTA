## Problem:

Let \(\mathbf{F}\) be a field. For m and n positive integers, let \(M\_{m\times n}\) be the vector space of \(m\times n\) matrices over \(\mathbf{F}\). Fix \(m\) and \(n\), and fix matrices \(A\) and \(B\) in \(M*{m\times n}\). Define the linear transformation \(T\) from \(M*{n\times m}\) to \(M*{m\times n}\) by*

\[T(X)=AXB.\]

Prove that if \(m\neq n\), then \(T\) is not invertible.

## Solution:

Let \(m\neq n\). We write \(T=T*{1}T*{2}\), where \(T*{2}:M*{n\times m}\to M*{m\times m}\) is defined by \(T*{2}(X)=BX\) and \(T*{1}:M*{n\times n}\to M*{m\times n}\) is defined by \(T*{1}(Y)=AY\). Since \(\dim M*{n\times m}=nm\geq n^{2}=\dim M*{n\times n}\), the transformation \(T\_{2}\) has a nontrivial kernel, by the spectral theorem. Hence, \(T\) also has a nontrivial kernel and is not invertible.

We write \(T=T*{2}T*{1}\), where \(T*{1}:M*{n\times m}\to M*{m\times m}\) is defined by \(T*{1}(X)=AX\) and \(T*{2}:M*{m\times m}\to M*{m\times n}\) is defined by \(T*{2}(Y)=BY\). Now we have \(\dim M*{n\times m}=nm\geq m^{2}=\dim M*{m\times m}\), so \(T\_{1}\) has a nontrivial kernel, and we conclude as before that \(T\) is not invertible.

