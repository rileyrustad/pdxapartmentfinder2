# -*- coding: utf-8 -*-
'''python module contains functions built to parse multnomah county craigslist apartment html
'''
# from future import division, print_function
import numpy as np
from bs4 import BeautifulSoup, NavigableString
import re


def attributes(soup):
    '''Parses HTML down to just the attributes of a listing.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    bedbathfeet : HTML that contains just the bedroom, bathroom, and square
    footage data.

    attributes : HTML that contains the additional attributes.
    '''

    # mapAndAttrs HTML tag has all of the uniform attributes
    summary = soup.find("div", {'class': 'mapAndAttrs'})
    # try:
    summary2 = summary.find_all("span")
    summary3 = summary.find_all("b")
    bedbathfeet = []
    attributes = []

    # All bolded attributes are number of baths, beds, or square feet
    for i in summary3:
        text = i.find(text=True)
        if text != 'open house dates':
            bedbathfeet.append(text)

    # The unbolded attributes are saved in a separate list
    for i in summary2:
        text = i.find(text=True)
        if text not in bedbathfeet:
            attributes.append(text)

    return bedbathfeet, attributes


def bedbathfeet(bedbathfeet):
    '''Find number of bedrooms, bathrooms, and square feet.

    Parameters
    ----------
    bedbathfeet : List containing number of bedrooms, bathrooms, and square
    footage. See GetAttributes

    Returns
    -------
    bedbathfeet : list with available in the format[# beds, # baths,
                                                    square feet]
    '''
    # Test to see if all intergers or if it contains a string
    bed, bath, feet = np.nan, np.nan, np.nan
    for item in bedbathfeet:
        if 'BR' in item:
            bed = int(item[0])
        elif 'Ba' in item:
            bath = int(item[0])
        else:
            feet = int(item)
    return bed, bath, feet


def price(soup):
    '''Finds price of a listing.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    price : int of listing price.
    '''
    # Parse down to just the price HTML tag
    summary = soup.find("span", {'class': 'price'})

    # Check to see if listing has a price.
    if summary == None:
        return np.nan

    # Return the price.
    else:
        text = summary.find(text=True)
        # Get rid of first $ character, and convert to int()
        price = int(str(text)[1:])
        return price


def smoking(attributes):
    '''Finds if a listing allows smoking.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    smoking : string of 'no smoking' or NaN value if none listed.
    '''
    for i in attributes:
        if str(i) == 'no smoking':
            return 1
        else:
            return 0


def furnished(attributes):
    '''Finds if a listing is furnished.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    smoking : string of 'furnished' or NaN value if none listed.
    '''
    for i in attributes:
        if str(i) == 'furnished':
            return 1
        else:
            return 0



def wheelchair(attributes):
    '''Finds if a listing is wheelchair accessible.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    smoking : string of 'furnished' or NaN value if none listed.
    '''

    for i in attributes:
        if str(i) == 'wheelchair accessible':
            return 1
        else:
            return 0


def laundry(attributes):
    '''Finds the laundry type a listing has.

    Parameters
    ----------
    attributes : Scraped HTML parsed down to just attributes of the listing.

    Returns
    -------
    a string of the type of laundry available or NaN value if none listed.
    '''
    for i in attributes:
        if str(i) == 'w/d in unit':
            return 'w/d in unit'
        elif str(i) == 'laundry in bldg':
            return 'laundry in bldg'
        elif str(i) == 'laundry on site':
            return 'laundry on site'
        elif str(i) == 'w/d hookups':
            return 'w/d hookups'
        elif str(i) == 'no laundry on site':
            return 'no laundry on site'
    else:
        return np.nan


def housing_type(attributes):
    '''Finds the housing type a listing has.

    Parameters
    ----------
    attributes : Scraped HTML parsed down to just attributes of the listing.

    Returns
    -------
    a string of the type of housing available or NaN value if none listed.
    '''
    for i in attributes:
        if str(i) == 'apartment':
            return 'apartment'
        elif str(i) == 'condo':
            return 'condo'
        elif str(i) == 'cottage/cabin':
            return 'cottage/cabin'
        elif str(i) == 'duplex':
            return 'duplex'
        elif str(i) == 'flat':
            return 'flat'
        elif str(i) == 'house':
            return 'house'
        elif str(i) == 'in-law':
            return 'in-law'
        elif str(i) == 'loft':
            return 'loft'
        elif str(i) == 'townhouse':
            return 'townhouse'
        elif str(i) == 'manufactured':
            return 'manufactured'
        elif str(i) == 'assisted living':
            return 'assisted living'
        elif str(i) == 'land':
            return 'land'
    else:
        return np.nan


def parking(attributes):
    '''Finds the parking type a listing has.

    Parameters
    ----------
    attributes : Scraped HTML parsed down to just attributes of the listing.

    Returns
    -------
    a string of the type of parking available or NaN value if none listed.
    '''
    x = []
    for i in attributes:
        if str(i) == 'carport':
            return 'carport'
        elif str(i) == 'attached garage':
            return 'attached garage'
        elif str(i) == 'detached garage':
            return 'detached garage'
        elif str(i) == 'off-street parking':
            return 'off-street parking'
        elif str(i) == 'street parking':
            return 'street parking'
        elif str(i) == 'valet parking':
            return 'valet parking'
        elif str(i) == 'no parking':
            return 'no parking'
    else:
        return np.nan


def available(soup):
    '''Finds the date a listing is available.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    a string of the date a listing is available.
    '''

    summary = soup.find("span", {'class': 'property_date'})
    if summary == None:
        return np.nan
    else:
        return summary['data-date']


def cat(attributes):
    '''Finds whether a listing allows cats.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    1 if the listing allows cats and a 0 if it doesn't
    '''
    if u'cats are OK - purrr' in attributes:
        return 1
    else:
        return 0


def dog(attributes):
    '''Finds whether a listing allows dogs.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    1 if the listing allows dogs and a 0 if it doesn't
    '''

    if u'dogs are OK - wooof' in attributes:
        return 1
    else:
        return 0


def deleted(soup):
    '''Finds whether a listing has been deleted since it's ID was scraped.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    If the listing has been removed, return false, or else return true.
    '''
    summary = soup.find("div", {'class': "removed"})
    if summary == None:
        return False
    else:
        return True


def content(soup):
    summary = soup.find("section", {'id': 'postingbody'})
    str(summary)
    # remove divs
    summary.div.extract()
    # remove html tags
    summary = re.sub(r'<.*?>', '', str(summary))
    # replace whitespace with just a single space.
    summary = re.sub(r'\n+', ' ', summary)
    summary = re.sub(r'\s+', ' ', summary)

    # Return both the Text and the number of words used to describe the listing.
    return summary, len(summary.split(' '))


def lat_lon(soup):
    '''Finds the lattitute and longitude coordinates for a listing

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    lat : a listings lattitude

    lon: a listings longitude
    '''

    summary = soup.find("div", {'id': 'map'})
    if summary == None:
        return np.nan, np.nan
    else:
        lat = summary["data-latitude"]
        lon = summary["data-longitude"]

    return lat, lon


def has_map(soup):
    '''Determines if a listing has a map.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    1 if it has a map, 0 if it doesn't
    '''
    summary = soup.find("div", {'class': 'mapbox'})
    if summary == None:
        return 0
    else:
        return 1


def photos(soup):
    '''Counts the number of photos a listing has.

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    Number of photos posted on the listing
    '''
    summary = soup.find("div", {'id': 'thumbs'})
    if summary == None:
        return 0
    else:
        summary2 = summary.find_all("a")
    return len(summary2)


def time_posted(soup):
    '''Determines when a posting was listed

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    The time a listing was posted.
    '''
    summary = soup.find("time", {'class': 'timeago'})['datetime']
    #format of summary is '2017-01-15T16:55:40-0800'
    summary = summary.split('T')
    time, _ = summary[1].split('-')
    return summary[0], time


def title(soup):
    '''Determines when a posting was listed

    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.

    Returns
    -------
    The time a listing was posted.
    '''
    summary = soup.find("span", {'id': 'titletextonly'})


    if summary == None:
        return np.nan
    else:
        text = summary.find(text=True)
        return text

#TODO: for anything with attributes use ```if 'str' in attributes``` rather than looping?
#TODO: fix all of ```== None``` comparisons