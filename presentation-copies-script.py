import requests
from lxml import etree
from datetime import datetime

# insert ####### share link from website or from library spreadsheet
# interruption example https://hansard.parliament.uk/Commons/2024-09-09/debates/EA3CE383-F88C-4A9B-B230-F2424184F408/Transport#contribution-ED93B984-A121-41FB-A611-8D2438E2E111
share_link = "https://hansard.parliament.uk/Commons/2024-10-10/debates/4D26F1DB-5194-49CD-85CF-087377B7A3DB/SportTeamGBAndParalympicsgb#contribution-B7C30195-448D-4087-9106-EDDC8FC517B7"

# splitting the share link #contribution-
string_split = share_link.split("#contribution-")

# second value out of a list of two 0,1
content_item_external_id = string_split[1]

# creating a variable which adds the string from above which is the external ID
find_debate_section_id_url = "https://hansard-api.parliament.uk/search/debatebyexternalid.json?contentItemExternalId={content_item_external_id}&house=Commons"

# formatting the variable with the externalid
ext_id_url = ((find_debate_section_id_url.format(content_item_external_id=content_item_external_id)))

# requesting the new URL
response = requests.get(ext_id_url)

# creating a variable with the response from the above request
DebateSectionExtId_data = response.json()

# use the response to get the DebateSectionExtId value
for item in DebateSectionExtId_data.get("Results", []):
    DebateSectionExtId = item.get("DebateSectionExtId")

# create URL that fetches the maiden speech content and the title of the speech

create_url = "https://hansard-api.parliament.uk/debates/debate/{DebateSectionExtId}.json"

url = ((create_url.format(DebateSectionExtId=DebateSectionExtId)))

# requesting the new URL
response_api = requests.get(url)

# creating a variable with the response from the above request
maiden_speech_data = response_api.json()

title = maiden_speech_data.get("Overview", [])

#
for item in maiden_speech_data.get("Items", []):
    if item.get("ExternalId") == content_item_external_id:
        speech = item.get("Value")
        debate_title = title.get("Title")
        time_code = item.get("Timecode")
        member_details = item.get("AttributedTo")

# adding extra info that can be automated later
chamber = "House of Commons"
speech_type = "The Maiden Speech"

# split atrributedto value into member name and details of member
member_name, cons, party = member_details.split(' (')
cons = cons.rstrip(')')  # Remove the trailing parenthesis
party = party.rstrip(')')  # Remove the trailing parenthesis

# convert time_code into datetime
dt = datetime.fromisoformat(time_code)

# re-format the date and time
formatted_date = dt.strftime("%d %B %Y")

hour = dt.strftime("%I").lstrip("0")  # Get hour and remove leading zero
formatted_time = f"{hour}.{dt.strftime('%M').lstrip('0')}{dt.strftime('%p').lower()}" 

# creating a list which splits on line break and removes empty paragraphs
para_list = [para for para in speech.split("\n") if para.strip()]

# Creating XML output, start with root
output_element = etree.Element('root')

speech_type_ele = etree.SubElement(output_element, 'speech_type')
speech_type_ele.text = speech_type.strip()

member_element = etree.SubElement(output_element, 'Member')
member_element.text = member_name.strip()

chamber_ele = etree.SubElement(output_element, 'chambers')
chamber_ele.text = chamber.strip()

time_element = etree.SubElement(output_element, 'date')
time_element.text = formatted_date.strip()

# adding title element
title_element = etree.SubElement(output_element, 'hs_2GenericHdg')
title_element.text = debate_title.strip()

# adding timecode element 
time_element = etree.SubElement(output_element, 'hs_Timeline')
time_element.text = formatted_time.strip()

# Create the member_details element
member_details = etree.SubElement(output_element, "member_details")

# Create and add the bold element for member name
bold_element = etree.SubElement(member_details, "bold")
bold_element.text = member_name

# Create the details element for constituency and party
details_element = etree.SubElement(member_details, "details")
details_element.text = f" ({cons}) ({party})"

# adding tag to each paragraph which is currently in a list
for paragraph in para_list:

    tag_name = "hs_Para"

    if paragraph.startswith('“'):
        tag_name = "hs_brev"

    speech_element = etree.fromstring(
        f"<{tag_name}>{paragraph.strip()}</{tag_name}>"
    )
    output_element.append(speech_element)

# adding em for inline styles within paragraph
for em in output_element.xpath("//em"):
    em.tag = "I"

for element in output_element.iterchildren():
    element.tail = "\n"

# gets member name for file name
member_name_split = member_name.split()
firstname = member_name_split[0]
lastname = member_name_split[1]

output_tree = etree.ElementTree(output_element)
output_tree.write(firstname + "_" + lastname + ".xml", encoding="utf-8")