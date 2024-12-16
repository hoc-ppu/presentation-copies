from datetime import datetime
from pathlib import Path

import requests
from lxml import etree
from lxml.etree import SubElement

MISSING_TITLE = "INSERT TITLE"

HANSARD_DEBATES_URL_BASE = "https://hansard-api.parliament.uk/debates/debate/"

# this function is the same as the presentation copies script
# turned into a function to use with tkinter GUI

# TODO: force speech empty error
# TODO: return line 46 and any others, create separate functions
# TODO: add instruction to screenshot/report error to documentation
# TODO: add raised exceptions as "e" for logger?

# TODO: consider adding a logger


def get_speech(share_link: str, output_folder: str) -> tuple[str, str, str]:

    """
    This function takes a share link from the production-gui and
    returns an XML file with the speech content.
    """
    try:
        # splitting the share link #contribution-
        url_string_split = share_link.split("#contribution-")
        # second value out of a list of two 0,1
        content_item_external_id = url_string_split[1]
    except Exception:
        raise Exception("Website Link (URL) is invalid. Nothing serious. This could just be a typo, try copy and pasting the link from Click Up again. If it doesn't fix it let the tech team know")
    """
    creating a variable which adds the string from above which is the
    external ID
    """

    ext_id_url = (
        "https://hansard-api.parliament.uk/search/"
        "debatebyexternalid.json?contentItemExternal"
        f"Id={content_item_external_id}&house=Commons"
    )
    # formatting the variable with the externalid
    try:
        # requesting the new URL
        response = requests.get(ext_id_url)
        # creating a variable with the response from the above request
        DebateSectionExtId_data = response.json()
    except Exception:
        raise Exception(f"Failed to fetch the Hansard Data.\n\nIf working from home check you're logged into the VPN and then check there isn't a typo in your website link.\n\n Copy and paste the link from Click Up and try again.\n\n\n If it doesn't fix it let the tech team know.\nGive tech team this link {ext_id_url}.")

    DebateSectionExtId = ""

    # use the response to get the DebateSectionExtId value
    for item in DebateSectionExtId_data.get("Results", []):
        DebateSectionExtId = item.get("DebateSectionExtId")

    if not DebateSectionExtId:
        raise Exception(
            f"Unable to find the debate information from the website link.\n\nCheck the website link for typos and try again.\n\n\nIf it doesn't fix it let the tech team know.\n\nGive tech team this link {ext_id_url}.")
    """
    create URL that fetches the maiden speech content and the
    title of the speech
    """
    create_url_template = "{}{}.json"
    url = create_url_template.format(HANSARD_DEBATES_URL_BASE, DebateSectionExtId)

    # fetching content from hansard API, program ends with error
    try:
        response_api = requests.get(url)
        # creating a variable with the response from the above request
        maiden_speech_data = response_api.json()
    except Exception:
        raise Exception(
            f"Unable to find the speech information from the website link.\n\nCheck the website link for typos and try again.\n\n\nIf it doesn't fix it let the tech team know.\n\nGive tech team this link {url}"
        )

    overview = maiden_speech_data.get("Overview", {})

    debate_title = ""

    # TODO: look at using logger instead of below
    warn_title = ""
    warn_datetime = ""
    warn_member_details = ""

    debate_title = overview.get("Title", "INSERT TITLE")
    if debate_title == "INSERT TITLE":
        warn_title = "No debate title in the data.Insert Debate Title manually"

    """
    Set default values of below items to none and empty
    Allows program to run with empty returns
    """

    time_code = None
    member_details = None
    speech = ""
    ext_id_found = False

    for item in maiden_speech_data.get("Items", []):
        if item.get("ExternalId") == content_item_external_id:
            ext_id_found = True
            """
            # added boolean check for error if contentID is not found in
            # results
            """

            speech = item.get("Value", "")
            if speech == "":
                raise Exception("Speech is missing from data")
            time_code = item.get("Timecode")
            member_details = item.get("AttributedTo")
            break
    # TODO: need to add multiple contributions and then
    #       concatenate them together.

    if ext_id_found is False:
        raise Exception("Website Link not working.\n\nCheck for a blank space or typo at end of URL and try again.\n\n\nContentExternalID not found")

    # adding extra info that can be automated later
    chamber = "House of Commons"
    speech_type = "Maiden Speech"

    member_name = "INSERT MEMBER NAME"
    cons = "INSERT CONSTITUENCY"
    party = "PARTY"

    if member_details:
        # split attributed to value into member name and details of member
        member_splits = member_details.split(" (")
        try:
            member_name = f"{member_splits[0]} MP"
            cons = member_splits[1]
            party = member_splits[2]

            # Remove the trailing
            cons = cons.rstrip(")")
            party = party.rstrip(")")
        except IndexError:
            # TODO: consider this warning message
            warn_member_details = "Member details incorrectly formatted in the data.\nDouble check the Member Name, Constituency and Party are correct in the document"
    else:
        warn_member_details = "No member details in the data. \nAdd the member name, constituency and party details manually in the indesign document."

    # convert time_code into datetime
    if time_code:
        dt = datetime.fromisoformat(time_code)
        formatted_date = dt.strftime("%d %B %Y")
        hour = dt.strftime("%I").lstrip("0")  # Get hour and remove leading zero
        formatted_time = (
            f"{hour}.{dt.strftime('%M').lstrip('0')}{dt.strftime('%p').lower()}"
        )
    else:
        formatted_date = "INSERT DATE"
        formatted_time = "INSERT TIME"
        warn_datetime = "No date or time in the data.\nEnter the date and time in the Indesign document manually"

    # creating a list which splits on line break and removes empty paragraphs
    para_list = [para for para in speech.split("\n") if para.strip()]

    # TODO: split out the XML creation into a separate function

    # Creating XML output, start with root
    output_element = etree.Element("root")

    speech_type_ele = SubElement(output_element, "speech_type")
    speech_type_ele.text = speech_type.strip()

    member_element = SubElement(output_element, "Member")
    member_element.text = member_name.strip()

    chamber_ele = SubElement(output_element, "chambers")
    chamber_ele.text = chamber.strip()

    time_element = SubElement(output_element, "date")
    time_element.text = formatted_date.strip()

    # adding title element
    title_element = SubElement(output_element, "hs_2GenericHdg")
    title_element.text = debate_title.strip()

    # adding timecode element
    time_element = SubElement(output_element, "hs_Timeline")
    time_element.text = formatted_time.strip()

    # Create the member_details element
    member_details = SubElement(output_element, "member_details")

    # Create and add the bold element for member name
    bold_element = SubElement(member_details, "bold")
    bold_element.text = member_name

    # Create the details element for constituency and party
    details_element = SubElement(member_details, "details")

    details_element.text = f" ({cons}) ({party}) "

    # adding tag to each paragraph which is currently in a list
    for paragraph in para_list:

        tag_name = "hs_Para"

        if paragraph.startswith("“"):
            tag_name = "hs_brev"

        speech_element = etree.fromstring(
            f"<{tag_name}>{paragraph.strip()}</{tag_name}>"
        )
        output_element.append(speech_element)

    # adding em for inline styles within paragraph
    for em in output_element.xpath("//em"):
        em.tag = "I"

    for element in output_element.iterchildren():
        if element.tag == "member_details":
            # Stuart does not want a new line after the details
            continue
        element.tail = "\n"

    if len(output_element) > 0:
        # The last element must not have a newline
        last_child = output_element[-1]

        if last_child.tail is not None:
            last_child.tail = last_child.tail.rstrip()

        if output_element.tail is not None:
            output_element.tail = output_element.tail.rstrip()

    # gets member name for file name
    # member_name_split = member_name.split()
    # firstname = member_name_split[0]
    # lastname = member_name_split[1]

    file_name = member_name.replace(" ", "_")

    output_file_path = Path(output_folder, f"{file_name}.xml")

    output_tree = etree.ElementTree(output_element)
    output_tree.write(
        str(output_file_path), encoding="utf-8", xml_declaration=True
    )

    # TODO: is this the best way, maybe use logger?
    return (warn_datetime, warn_title, warn_member_details)
