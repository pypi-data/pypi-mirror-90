from setuptools import setup

version = {}

with open('slack_rtm_bot/__version__.py', 'r') as f:
  exec(f.read(), version)

with open('README.md', 'r') as f:
  readme = f.read()

setup(
    name='slack-rtm-bot',
    version=version['__version__'],
    description='Slack RTM bot',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/nkouevda/slack-rtm-bot',
    author='Nikita Kouevda',
    author_email='nkouevda@gmail.com',
    license='MIT',
    packages=[
        'slack_rtm_bot',
        'slack_rtm_bot.handlers',
    ],
    install_requires=[
        'requests',
        'slackclient',
        'websocket-client',
    ],
    entry_points={
        'console_scripts': [
            'slack-rtm-bot=slack_rtm_bot.__main__:main',
        ],
    },
)
