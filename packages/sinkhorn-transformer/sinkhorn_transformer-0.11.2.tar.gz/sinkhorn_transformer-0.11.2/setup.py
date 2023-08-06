from setuptools import setup, find_packages

setup(
  name = 'sinkhorn_transformer',
  packages = find_packages(exclude=['examples']),
  version = '0.11.2',
  license='MIT',
  description = 'Sinkhorn Transformer - Sparse Sinkhorn Attention',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/sinkhorn-transformer',
  keywords = ['transformers', 'attention', 'artificial intelligence'],
  install_requires=[
      'torch',
      'product-key-memory',
      'axial-positional-embedding>=0.1.0'
  ],
  classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
  ],
)
