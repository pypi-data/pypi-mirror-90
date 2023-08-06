from setuptools import setup


setup(
    name='skcvideo',
    version='0.1.4',
    description='video utils',
    author='SkillCorner',
    author_email='timothe.collet@skillcorner.com',
    license='MIT',
    packages=[
        'skcvideo',
    ],
    install_requires=[
        'click>=7.1.2',
        'numpy>=1.18.5',
        'opencv-python>=4.4.0.46',
        'imageio>=2.9.0',
        'imageio-ffmpeg>=0.4.2',
    ])
