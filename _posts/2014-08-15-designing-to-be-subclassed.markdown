---
layout: post
title: "Designing to be Subclassed"
date: 2014-08-15 09:00:05 -0400
comments: true
categories: 
- design
- open source

---

We've reached an interesting stage of the development of the first ParagonMeasure product. As a mobile health telemonitoring tool with immediate research applications, I've been asked to take the analysis library which I wrote over much of June and July and build it into a web application. This presents a number of exciting challenges; the biggest being the challenge of taking a tool meant to run locally and give it the brains to run online.

Other facets of the challenge (dealing with [environments](https://kronosapiens.github.io/blog/2014/07/22/setting-up-virtual-environments-in-python/), [packaging](https://kronosapiens.github.io/blog/2014/07/28/understanding-package-imports-in-python/), [databases](https://kronosapiens.github.io/blog/2014/07/29/setting-up-unit-tests-with-flask/), caching, and the API) are fascinating, and dealt with in other posts. This post is going to be about the challenge of adapting classes and models to meet new requirements -- in a word, about *[subclassing](https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming))*.

<!--more-->

When architecting the web app, I made the call to preserve the original analysis library as it was, preserving all of the local functionality so that future researchers and developers could install the library to manage data and run analysis locally. This meant that rather than changing the original library to meet the new requirements, adapting the library for use on the web would require me to *subclass* the original classes and *override* all of the filesystem I/O methods and replace them with methods which interact with web APIs and noSQL databases.

As Sandi Metz repeatedly emphasizes in her [excellent book](http://www.poodr.com/), good software engineering is future-proof; good design is designed to be changed. While going through the process of subclassing my own library, I saw first-hand why best practices exist the way that they do. Several innocent decisions made in the initial library proved to be hindrances when it came time to extend functionality; getting to solve those problems from both sides (having full control over both the library and the web app) meant that I got to see the interaction first-hand. Without further ado, here are some insights:

## Declaring all instance varaibles in `__init__`

This first point is very much the low-hanging fruit of this post.

They say that you'll be shocked by how much you forget about the code you write, weeks or even days after the fact. *"What did I mean by that?"* is a common refrain. They say that the best code is written for humans, not machines, and as such should prioritize clarity above all. What this means in the context of this discussion is that you should *set all your instance variables when you initialize an object*. This means two things:

**First**, initialize any placeholder values, even if it's `None` or `[]` or `{}`. Even if you're not planning on using it until later, define it in `__init__` so that you'll remember it exists.

Here's an antipattern: you may think you won't need variable X until method C, so you go ahead and initialize it for the first time at the beginning of C. But say a user subclasses your object and decides they want to use X in method B. But now they're getting an exception and they need to figure out why. Now they have to both set variable X at the top of their method B, as well as override method C to *remove* the setting of X there (which would delete their version from method B). Further, if they ever decide that they actually want to run method C before method B, for whatever reason, they'll have to go back and add some sort of conditional in method B so they don't override the value of X from method C. This is all a huge and unecessary headache.

Initialize your variables once, in `__init__`, so they'll be there when you need them, and you won't have to struggle remembering what *order* you ***expected*** your users to want to do things. Requirements change, emergent behavior emerges. Don't confuse yourself and shackle yourself to a single use-case by obscuring what variables your objects depend on.

**Second**, don't write functions which run in `__init__` and set instance variables internally to themselves. You'll confuse the hell out of everyone, as people will have to remember *which* variables are set by *which*, since they can't tell by looking at `__init__`. Take a cue from the functional programmers and have those functions *return* their values and set those return values explicitly in `__init__`. Consider the following example:

```python
class Device(object):

    def __init__(self, subject_id):
        self.subject_id = subject_id
        self.device_dir = 'data/devices/'
        self.path = self.device_dir + subject_id + '_device.csv'
        self.create_device()
```
Things are actually looking fine until we get to that last line -- `self.create_device()` looks like it's doing some heavy duty lifting, but we can't tell by looking at `__init__`. We have to go down to where `create_device` is defined to see what variables it's setting:

```python
    def create_device(self):
        """Create the device dataframe"""
        self.get_device_dimensions()
        try:
            raw_device = pd.read_csv(self.path, sep='<>', skiprows=[0,1])
        except:
            raw_device = pd.read_csv(self.device_dir+'default_device.csv',
                                     sep='<>', skiprows=[0,1])
        raw_device = self.add_key_data(raw_device)
        self.data = raw_device.set_index('key', drop=False)
```

So it seems like it's setting `self.data`. It would've been much clearer if `create_device` had just `return`ed `raw_device.set_index('key, drop=False)`, and our `__init__` looked more like this:

```python
class Device(object):
    def __init__(self, subject_id):
        self.subject_id = subject_id
        self.device_dir = 'data/devices/'
        self.path = self.device_dir + subject_id + '_device.csv'
        self.data = self.create_device()
```
This is much clearer for both some other developer trying to subclass your library, as well as for *future you*, an important but often ignored part of your life. 

For those of you looking closely, you may have noticed some *bonus weirdness.* Go back and look at the first line of `create_device()`:

```python
    def create_device(self):
        """Create the device dataframe"""
        self.get_device_dimensions()
```

What is this? `get_device_dimensions()`? What does that do? What does that return? Now I have to go read some *more* source code? What kind of terrible developer are you? Let's peek:

```python
    def get_device_dimensions(self):
        """Get the device dimensions in pixels and millimeters"""
        try:
            f = open(self.path)
        except:
            f = open(self.device_dir+'default_device.csv')
        self.px_size = f.readline().rstrip().split(' ')[-1]
        self.mm_size = f.readline().rstrip().split(' ')[-1]
```
*You're kidding me*. You just set *two more instance variables* and said *nothing*. There should be a fine for this sort of malfeasance.

Let's take a few breaths and look at the refactored new hotness:

```python
class Device(object):
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.device_dir = 'data/devices/'
        self.path = self.device_dir + participant_id + '_device.csv'
        self.px_size, self.mm_size = self.get_device_dimensions()
        self.keys = self.create_device()
```
Such clarity. Such ease-of-subclassing. Such justice.

## Using Constants

One of the first modules I wrote in the library was `session_parser.py`, defining the `SessionParser` class capable of parsing CSV files and creating pandas DataFrames based on their contents.

The parser would go row-by-row through the CSV, pull out some of the fields, convert them to dictionaries, and then do further work on the values in the dictionaries. This meant that `SessionParser` needed to store some knowledge of the structure of the CSV and the interior dictionaries -- specifically, knowledge about the *keys*.

My original `session_parser.py` looked something like this:

```python
... # More imports
import re  # Python Regular Expression library


class SessionParser(object):
    """Object which can parse CSVs of typing data."""
    
	...
	
def parse_row(self, row):
        """Parse all typing data in a single row."""
        self.current_subject = row['user:id']
        self.current_device = self.load_device(self.current_subject)
        self.current_submit_time_str = row['context:timestamp']
        current_submit_time = pd.to_datetime(self.current_submit_time_str) 
        # Creates a pandas.tslib.Timestamp
        
	... # More stuff
```

This was fine for a while -- all my data was coming from the same source, so I naively hard-coded all of the keys right into the methods. Things changed once we went online, though. Data was coming from a web service via an API, not from CSVs stored locally. The data was *mostly* the same, but there were a number of small differences in convention and structure... including, of course, in the CSV column names and dictionary keys.

I needed to find some way for the library running locally to use one set of keys, with the subclassed parser using another. The answer, of course, was to extract the hard-coded keys out of the methods and store them as CONSTANTS at the top of the file, with the code itself just referencing the constants. This is a best practice, I think, for two reasons:

1. [The keys are stored in *one* place](https://en.wikipedia.org/wiki/Single_Source_of_Truth). Changing the key means changing the value of the constant once, versus changing it in multiple places all over the code.
2. Subclassed parsers can redefine the constants without having to change any of the actual method logic.

My new `session_parser.py` looks more like this:

```python
... # More imports
import re  # Python Regular Expression library

USER_ID_KEY = 'user:id'
TIMESTAMP_KEY = 'context:timestamp'
SESSION_KEY = 'finemotortest'

class SessionParser(object):
    """Object which can parse CSVs of typing data."""
    
    ...
    
    def parse_row(self, row):
        """Parse all typing data in a single row."""
        self.current_participant = row[USER_ID_KEY]
        self.current_device = self.load_device(self.current_participant)
        self.current_submit_time = pd.to_datetime(row[TIMESTAMP_KEY])
        # Creates a pandas.tslib.Timestamp
        
        ... # More stuff
```

Meanwhile, the subclassed version, `OhmageParser`, looks like this:

```python
... # More imports
from webapp import db

# Ohmage API query parameters
USER_ID_KEY = 'urn:ohmage:user:id'
SESSION_ID_KEY = 'urn:ohmage:survey_response:id'
TIMESTAMP_KEY = 'urn:ohmage:context:timestamp'
RESPONSE_KEY = 'urn:ohmage:prompt:response'
CONTEXT_KEY = 'urn:ohmage:context:launch_context_long'
# Not part of the API call, but in the response:
SESSION_KEY = 'urn:ohmage:prompt:id:finemotortest'

class OhmageParser(SessionParser):
    """Object wich can parse JSONs of typing data from the Ohmage API"""
    
	...

    def parse_row(self, row):
        """Parse all typing data in a single row."""
        self.current_session = self.create_session(row)
        self.current_participant = self.current_session.participant.name
        self.current_device = self.current_session.device
        # Assignments to satisfy the conventions of the parent class.
        self.current_submit_time = pd.to_datetime(row[TIMESTAMP_KEY])
        ...
        
    def create_session(self, row):
        s = Session(row[SESSION_ID_KEY], pd.to_datetime(row[TIMESTAMP_KEY]))
        s.participant = self.create_or_load_participant(row)
        s.device = self.create_or_load_device(row)
        s.save()
        return s

    def create_or_load_participant(self, row):
        p = Participant.query.filter_by(name=row[USER_ID_KEY]).first()
        if not p:
            p = Participant(row[USER_ID_KEY])
            p.save()
        return p

```
You'll notice a number of things here. The first is that I've redefined the keys by changing the constants at the top of the module. This means that methods defined in `session_parser.py` can run in the subclass of `OhmageParser` without any problem. The second is that I've actually overridden the `parse_row()` method. I've done this because `parse_row()` implements some I/O functionality that required some more heavy-duty customization. This is the subject of the next session.

## Interface methods, public methods, internal methods

This last section is more conceptual, and has to do with how your organize the functionality in your classes.

When I was subclassing my own library, I wanted to override as few methods as possible. Every override **doubles** the amount of code that needs to be maintained (since any big changes in the method need to be reflected on both the parent and child definitions), and feels like a personal design failure (at least for me).

Further, an override is a signal that the child class has different needs from the parent class -- a few of these may be necessary, but too many may suggest that you haven't thought through inheritence structure enough.

While going through this subclassing process, I discovered that there was a certain elegant and emergent clustering of methods into three categories:

#### Interface Methods

These are the methods most appropriate for subclassing. These are the Input/Output methods, which take input from external sources and convert them into formats which the class can work with internally, a bit like this:

input_method(outside_data) >> something the class understands >> output_data(internal_data) >> something the outside world understands.

In my case, moving from local to the web meant that I need to override the methods which took data from the filesystem with methods which could pull data from a web service's API. Further, I needed to be able to **write** data to a database, instead of to local files. By organizing this I/O functionality into methods separate from the core public and internal methods, I could override *just those* methods to get my classes working in their new environments.

For example, consider my `save_dataframe()` method from `SessionParser` (**Note**: I still need to implement functionality for saving two kinds of data -- something I've done on the new version but not the original):

```python
    def save_dataframe(self, parsed_row):
        """Save (create or update) participant data as appropriate."""
        # NOTE: NOT IMPLEMENTED DUAL TASK/MOTION DATAFRAMES
        dataframe = parsed_row['task_dataframe']
        participant_id = parsed_row['participant_id']
        try:
            prior_dataframe = pd.read_pickle(self.storage_dir + participant_id)
            output_dataframe = pd.concat([prior_dataframe, dataframe])
        except:
            output_dataframe = dataframe
        finally:
            (output_dataframe.sort(columns=['SubmitTime', 'Task', 'TouchTime']).
                to_pickle(self.storage_dir + participant_id)) 
            # Saves a pandas DataFrame locally as a 'pickle' 
```


Compare with the overriden method in `OhmageParser`, the child class:

```python
    def save_dataframe(self, parsed_row):
        """Write new data to the database."""
        if parsed_row['task_dataframe'] is not None:
            self.save_typing_data(task_dataframe)
        
        if parsed_row['motion_dataframe'] is not None:
            self.save_motion_data(parse_row)

    def save_typing_data(self, task_dataframe):
        task_dataframe['session_id'] = self.current_session.mongo_id
        task_dataframe['participant_id'] = self.current_session.participant.mongo_id
        typing_data_list = task_dataframe.to_dict(outtype='records')

        db.session.db.TypingData.insert(typing_data_list)
        # Saves the data as a series of Documents in a MongoDB database.

    def save_motion_data(self, motion_dataframe):
        motion_dataframe['session_id'] = self.current_session.mongo_id
        motion_data_list = motion_dataframe.to_dict(outtype='records')

        db.session.db.MotionData.insert(motion_data_list)
```

You'll note how the same method signature (`save_dataframe(self, parsed_row)`) means that the core methods inherited from the parent class don't need to know about the implementation of this method -- the child can override the method to deal with new storage requirements, but as long as it keeps the function signature the same, inherited methods will work just fine.

### Internal Methods

These are methods which the class uses internally for various tasks, but are generally not called by the user directly. I found that I would occasionally need to override these to account for the new environment I was in, even though these weren't pure I/O methods.

One example was `SessionParser`'s `is_already_parsed()` method. In the parent class, this method would reference a dictionary of already-seen dataframes to establish whether or not a new row had been parsed. The child class, `OhmageParser`, since it was pulling data from an API and could constrain the query by dates, could ensure that it was seeing only new data by specifying a recent time period. This method was called by the `parse_all()` method, which is the principal public method of the parent class (and the one that I definitely didn't want to have to override), which meant that I needed to do something like this:

```python
    def is_already_parsed(self, row):
        """Unecessary b/c Ohmage can be queried w/ date range."""
        return False
```

By overriding (and essentially neutralizing) an internal method, without changing it's method signature, I was able *adapt* the behavior of the parent class's methods *without* overriding them.

### Public Methods

These are the good-looking, outward facing prom kings and queens of your class. These are the methods that people will come to know and love. These should be as powerful and generic as possible. Most importantly, **their inputs and outputs should rarely, if ever change.**
	
Well, maybe not never. But *very rarely*. These public methods are what form the API, the interface, between your classes and the rest of the universe. They're how other people will learn to interact with your class. When people start using your library as part of their project, *these methods are what they will add to their code*. This means that if you screw around with these methods, everyone who is using your library will have to change their code.

To avoid that, these methods should be quite general-purpose, with lots of optional arguments and flags so people can tweak behavior while still working within the boundaries that the method defines.

For **inputs**, this means using lots of optional, keyword arguments with default values. This way, you can add functionality to your class without breaking backwards compatibility. If you can come up with a sensible default for any new parameter, you can expand the functionality of your public methods *without* breaking backward-compatibility.

That's inputs. What about outputs? This brings us nicely to the last point:

## Dictionaries are the Best Return Value

They're such a good return value it's almost too hard to believe. Think about it this way: if you return a dict, then the recieving function knows to access whatever value they want by using the correct key. As long as you don't change the *name of the dict* or *the name of the key* then you can add literally **anything** you want to that dictionary without breaking backwards-compatibility.

Here's a good example. Consider the old, busted version:

```python
    def convert_raw_session_to_dataframe(self, raw_session):
        """Convert a JSON of fine motor test data into a DataFrame."""

	... # About a dozen lines of pure brilliance
        
        if task_dataframes:
            return pd.concat(task_dataframes)
        else:
            return False
```
Ok, so assuming my `task_dataframes` list isn't empty (which happens, live data can be treacherous), I squeeze it all into a single DataFrame and return that sucker. The result gets recieved like this:

```python
    def parse_row(self, row):
        """Parse all typing data in a single row."""
	
	... # More brilliance

        session_dataframe = self.convert_session_fmt_to_dataframe(raw_session)

        if session_dataframe is not False:
            session_dataframe['SubmitTime'] = current_submit_time
            session_dataframe = session_dataframe.set_index(['SubmitTime'], drop=False)
        return session_dataframe, self.current_subject
```
Note that `parse_row` expects `convert_raw_session_to_dataframe` to return **one** DataFrame. It then does some further work and returns a **tuple** of the DataFrame and the current_subject.

Going up one more level, let's see how it comes together:

```python
    def parse_file(self, check_parsed=True):
        """Parse each row in a CSV file"""

            fmt_dataframe, subject_id = self.parse_row(row)
            if fmt_dataframe is not False:
                self.save_dataframe(fmt_dataframe, subject_id)
```
Ok, so `parse_file` expects to get a tuple back from `parse_row`. Of course, this entire design is stupid. Why? Because the minute I needed to add something -- say, for example, a second DataFrame, the entire thing fell apart. I needed to change *every* call to `convert_raw_session_to_dataframe` to expect a tuple of DataFrames, and *every* call to `parse_row` to give back a tuple of two DataFrames and a user. Ridiculous.

Fortunately, a better solution presented itself *immediately*:

```python
    def convert_raw_session_to_dataframes(self, session_dict):
        """Convert a dict of session data into a multi-task DataFrame."""

	... # Nobel-prize winning algorithmic brilliance
 
        return {'task_dataframe': task_dataframe,
            'motion_dataframe': motion_dataframe}
```
Gosh, that was easy. Let's go up a level:

```python
    def parse_row(self, row):
        """Parse all typing data in a single row."""
  	
	... # Pure poetry

        parsed_row = self.convert_raw_session_to_dataframes(session_dict)

        parsed_row['participant_id'] = self.current_participant
        return parsed_row
```
Oh, neat. I want to add something to the return value? Just toss that sucker in the dict.

```python
    def parse_all(self, check_parsed=True):
        """Parse each row in a pandas DataFrame.""""
    
	... # I think I've used this joke up

            parsed_row = self.parse_row(row)
            if (parsed_row['task_dataframe'] is not None or
                parsed_row['motion_dataframe'] is not None):
                self.save_dataframe(parsed_row)
```
Wow. So you're saying that I can now add *anything* I want to this `parsed_row` dictionary to meet virtually *any* new requirement without having to make *any* changes to existing code?

Neat.
