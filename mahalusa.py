import csv
import uuid
import textwrap
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.filterwarnings("ignore")


def insert_gossip_on_template(template_path, csv_path, output_dir):
    # Load the gossip data from the CSV file
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        gossip_data = list(reader)

    # Set the font style and size
    font_size = 30
    font = ImageFont.truetype('woodland-light.otf', size=font_size)
    font_committee = ImageFont.truetype('woodland-bold.otf', size=font_size)

    # Insert each gossip onto the template
    for data in gossip_data:
        committee = data['Which committee are you?']
        gossip = data['Gossip?']
        timestamp = data['Timestamp'] 

        if timestamp <= '2023/06/23 2:33:01 pm EEST':
            continue

        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)

        # Calculate the starting position for the gossip text to be centered vertically
        # start_y = (template.height - total_height) // 2 + 50

        # Insert committee at specific coordinates
        committee_width, committee_height = draw.textsize(committee, font=font_committee)
        committee_x = (template.width - committee_width) // 2

        committee_y = 450
        draw.text((committee_x, committee_y), committee, fill='white', font=font_committee)

        # Word wrap the gossip text
        wrapped_text = textwrap.wrap(gossip, width=30)  # Adjust the width as needed

        # Insert wrapped gossip text
        x = template.width // 2  # Center of the template
        y = 270
        line_height = font.getsize('hg')[1]  # Height of a line in the font
        for line in wrapped_text:
            line_width, _ = font.getsize(line)
            line_x = x - (line_width // 2)  # Adjust the position to center the line
            draw.text((line_x, y), line, fill='white', font=font)
            y += line_height

        # Generate a unique filename using UUID
        output_filename = str(uuid.uuid4()) + '.jpg'

        # Save the resulting image
        output_path = output_dir + output_filename
        template.save(output_path)
        print(timestamp)


# Example usage
template_path = 'template.jpg'
csv_path = 'Gossip box.csv'
output_dir = './output/'

insert_gossip_on_template(template_path, csv_path, output_dir)
