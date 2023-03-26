import re


def genres_choices():
    return [
        ("Alternative", "Alternative"),
        ("Blues", "Blues"),
        ("Classical", "Classical"),
        ("Country", "Country"),
        ("Electronic", "Electronic"),
        ("Folk", "Folk"),
        ("Funk", "Funk"),
        ("Hip-Hop", "Hip-Hop"),
        ("Heavy Metal", "Heavy Metal"),
        ("Instrumental", "Instrumental"),
        ("Jazz", "Jazz"),
        ("Musical Theatre", "Musical Theatre"),
        ("Pop", "Pop"),
        ("Punk", "Punk"),
        ("R&B", "R&B"),
        ("Reggae", "Reggae"),
        ("Rock n Roll", "Rock n Roll"),
        ("Soul", "Soul"),
        ("Other", "Other"),
    ]


def state_choices():
    return [
        ("AL", "AL"),
        ("AK", "AK"),
        ("AZ", "AZ"),
        ("AR", "AR"),
        ("CA", "CA"),
        ("CO", "CO"),
        ("CT", "CT"),
        ("DE", "DE"),
        ("DC", "DC"),
        ("FL", "FL"),
        ("GA", "GA"),
        ("HI", "HI"),
        ("ID", "ID"),
        ("IL", "IL"),
        ("IN", "IN"),
        ("IA", "IA"),
        ("KS", "KS"),
        ("KY", "KY"),
        ("LA", "LA"),
        ("ME", "ME"),
        ("MT", "MT"),
        ("NE", "NE"),
        ("NV", "NV"),
        ("NH", "NH"),
        ("NJ", "NJ"),
        ("NM", "NM"),
        ("NY", "NY"),
        ("NC", "NC"),
        ("ND", "ND"),
        ("OH", "OH"),
        ("OK", "OK"),
        ("OR", "OR"),
        ("MD", "MD"),
        ("MA", "MA"),
        ("MI", "MI"),
        ("MN", "MN"),
        ("MS", "MS"),
        ("MO", "MO"),
        ("PA", "PA"),
        ("RI", "RI"),
        ("SC", "SC"),
        ("SD", "SD"),
        ("TN", "TN"),
        ("TX", "TX"),
        ("UT", "UT"),
        ("VT", "VT"),
        ("VA", "VA"),
        ("WA", "WA"),
        ("WV", "WV"),
        ("WI", "WI"),
        ("WY", "WY"),
    ]


def is_valid_phone(number):
    """Validate phone numbers like:
    1234567890 - no space
    123.456.7890 - dot separator
    123-456-7890 - dash separator
    123 456 7890 - space separator

    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -.  = ?[-. ]

    Note: (? = optional) - Learn more: https://regex101.com/
    """
    regex = re.compile("^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$")
    return regex.match(number)
