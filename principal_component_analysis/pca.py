import numpy as np


class PCA:
    """
    Numpy implementation of Principal Component Analysis.
    """

    def __init__(self, n_components: int, solver='svd'):
        self.n_components = n_components
        self.solver = solver
        self.components = None
        self.vectors = None

    def fit(self, X: np.ndarray):
        """
        Calculates the eigenvectors and eigenvalues for PCA computation.

        :param X: An array of features
        :return: None
        """
        x = np.array(X)
        zero_mean = x - x.mean(axis=0)

        if self.solver == 'svd':
            self.fit_svd(zero_mean)
        else:
            self.fit_cov(zero_mean)

    def fit_cov(self, X: np.ndarray):
        """
        Calculates the eigenvalues and eigenvectors using the covariance
        matrix.

        :param X: An array of zero mean features
        :return: None
        """
        cov = np.cov(X.T)  # same as (X.T @ X) / (n - 1)

        # Matrix Decomposition
        components, vectors = np.linalg.eig(cov)
        idx = components.argsort()[::-1]  # Sorted in descending order
        self.components = components[idx]
        self.vectors = vectors[idx]

    def fit_svd(self, X: np.ndarray):
        """
        Calculates the eigenvalues and eigenvectors using Singular Value
        Decomposition.
        :param X: An array of zero mean features
        :return: None
        """
        U, sig, V = np.linalg.svd(X)
        self.vectors = V
        self.components = np.square(sig) / (X.shape[0] - 1)

    def transform(self, X: np.ndarray):
        """
        Projects the input data along the principal components of fitted data.

        :param X: An array of features
        :return: n by n_components matrix
        """
        return (X - X.mean(axis=0)).dot(self.vectors.T)  # Projection

    def fit_transform(self, X: np.ndarray):
        """
        Calculates the eigenvalues and eigenvectors using supplied method.
        Projects the input data along the principal components of fitted data.

        :param X: An array of features
        :return: n by n_components matrix
        """
        x = np.array(X)
        zero_mean = x - x.mean()

        if self.solver == 'svd':
            self.fit_svd(zero_mean)
            return self.transform(x)

        self.fit_cov(zero_mean)
        return self.transform(x)

    @property
    def explained_variance(self):
        """
        Calculates the explained variance by selecting up to the nth component.
        :return: np.float
        """
        return self.components[
               :self.n_components].sum() / self.components.sum()


if __name__ == '__main__':
    from sklearn.datasets import load_breast_cancer
    from sklearn.decomposition import PCA as PCA_sklearn
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    cancer = load_breast_cancer()
    data = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    data["label"] = cancer.target
    X = data.drop("label", axis=1).values

    # ---------------My PCA--------------------------------------------------#
    pca = PCA(2)
    pca.fit(X)
    tran = pca.transform(X)

    sns.scatterplot(tran[:, 0], tran[:, 1],
                    hue=data.label.map({1: "Malignant", 0: "Benign"}))
    plt.title("My implementation")
    plt.show()
    print("Explained variance is", pca.explained_variance.round(3))
    # ---------------My PCA--------------------------------------------------#

    # ---------------Sklearn PCA---------------------------------------------#
    p = PCA_sklearn(2, svd_solver='full')
    p.fit(X)
    transformed = p.transform(X)

    sns.scatterplot(transformed[:, 0], transformed[:, 1],
                    hue=data.label.map({1: "Malignant", 0: "Benign"}))
    hue = data.label.map({1: "Malignant", 0: "Benign"})
    plt.title("Sklearn implementation")
    plt.show()
    print("Explained variance is", p.explained_variance_ratio_.sum().round(3))
    # ---------------Sklearn PCA---------------------------------------------#
