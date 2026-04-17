from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import SiteSettings, Testimonial
from properties.models import (
    Agent,
    Amenity,
    Location,
    Property,
    PropertyFeature,
    PropertyImage,
    PropertyType,
)


LOCATIONS = [
    ("St. Tropez", "", "France"),
    ("Aspen", "Colorado", "United States"),
    ("Malibu", "California", "United States"),
    ("Siena", "Tuscany", "Italy"),
    ("Manhattan", "New York", "United States"),
    ("Joshua Tree", "California", "United States"),
    ("Montecito", "California", "United States"),
    ("Kyoto", "", "Japan"),
    ("Oxfordshire", "", "United Kingdom"),
]

TYPES = [
    "Modernist Villa",
    "Heritage Manor",
    "Minimalist Loft",
    "Coastal Estate",
    "Modern Penthouse",
    "Historic Manor",
]

AMENITIES = [
    ("Private Vineyard", "nature"),
    ("Infinity Pool", "pool"),
    ("Helipad", "flight"),
    ("Chef's Kitchen", "restaurant"),
    ("Wine Cellar", "liquor"),
    ("Home Theater", "theaters"),
    ("Private Gym", "fitness_center"),
    ("Smart Home", "home_iot_device"),
]

AGENTS = [
    {
        "name": "Julian Vane",
        "role": "Managing Partner",
        "email": "julian@apertureestate.com",
        "phone": "+44 20 7946 0128",
        "photo_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBXFnTuoAjMLSH0zEVlLbJfVRJiKpjO51FZpH4YrCxDF1dW5rfWwkStY0dY1zWnKSUW2pVCAOy6REA0cCJaBO7UqMAXWurUk8BdYjsXcxEZE-hwkl0m7KJJnQz6wAnllBErEn9i_hTjKsq05Ff8TI_MOx5AJ7lLkHLKkKquFvbtnfj5E_BfkC-B_yKXnacOac8V-PAyyA75Jx6C8HLRCy99K9L55iCwilCVQZB4KcpvNO6cHWo0N5IOVr4MJGSTkz05A5TCMp-PP48",
        "featured": True,
        "order": 1,
    },
    {
        "name": "Elena Thorne",
        "role": "Senior Consultant",
        "email": "elena@apertureestate.com",
        "phone": "+44 20 7946 0129",
        "photo_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBtIhaJ0xPHya5GIaMggbIMp2aQ5Ao689sGUlmwlFw490CXkQNP0D8-qUMvbZLOAdAYJls6CwaHIvAd0vnNNiAeUT1I7GEJsXuA5Unvm6T_9iy0L8dzVKjR2iK9g8f1ketX1laq-wa3Dw0L2SUGoQAjQO09QJ_qGI4Khq1dDUtVFrKbSV7U6OGX6n1ogP5K7e-1lyUD2Sx5kdbS1UPBQSX-gMyOItO4gxqQQxToauL6tDK-3RhWYhz2zOs-ClN7G-RIg28Yzw0Fkw4",
        "featured": True,
        "order": 2,
    },
    {
        "name": "Marcus Sterling",
        "role": "Head of Acquisitions",
        "email": "marcus@apertureestate.com",
        "phone": "+44 20 7946 0130",
        "photo_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAb-nPetKv7raZj9BWwLQNMuteLJ33Pf2EMZUMBsIC1fGFSCaRd9gQxyULRo2RtDDy3kVpEcwivY7GSUZHc8OnxFX3FQkdq18LuOfCsVFCir9OhxDx3UTlbzLx6WWDghfPTkemoWvYjQIyitG4_d591rkp03m1B5bvgfnM9eizlGR9fxkBaTr8e7f8rS4nKqGeXVYE1kJUWwh-Bj7UdPcQaJZ7JR8rvKFQ-fDCcRRnVXoKXW0Bi2OL8c9b5cCtl2_LBPnhW-5K1lf8",
        "featured": True,
        "order": 3,
    },
    {
        "name": "Sophia Aris",
        "role": "Design Liaison",
        "email": "sophia@apertureestate.com",
        "phone": "+44 20 7946 0131",
        "photo_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCDhVwTLjWw_-VdDwxeHJ7nk8UUaqWQrNKyAagX1ninkohvhd_i9vjxXdKNy8c9H44J8SQ9i4whqHmfq3cpAr-QPgLKVNwEebPRK3-iDx9qrqHURZyVeRImR88Skm_TVq-FL5jjyhZf-B2LGti77vaIBjO5kStnvYQdMYTwaOH5UQHJTpZFYZ-AIUZY2tbm9kMbu6Rgi5LrwNUTQbh970CBv29LkukEaA8qrhGfUYIFCp2cND0KgFZppl1mBt1GqDTNp0at-4FfOwc",
        "featured": True,
        "order": 4,
    },
]

PROPERTIES = [
    {
        "title": "The Alabaster Pavilion",
        "tagline": "Premium Listing",
        "location": ("St. Tropez", "France"),
        "type": "Modernist Villa",
        "status": "exclusive",
        "price": Decimal("18500000"),
        "bedrooms": 6,
        "bathrooms": 8,
        "square_feet": 12400,
        "garage_spaces": 4,
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuA1rIxc-oveHGkBBv6D7W7rmCwd1y-TO9wdTnqZktG4lfeHmq0DJCKgdK7AOlYUXN8Ungw9pOwjCNfpCXdw6CHhy9CO0D9ozmZrU6J3lUIanP6xsZwXRdbocjWg5UbQdwbJifjoaIbGUE2yAQQBIiEj2JTDCa80nDp2SAJvbWQMFP4f3R9t27gbePunmq30MZoKaxS4kfsO-koxW9P4bGeplYZ7kyxjSWMqcM9DzB1-ohEPSqilYkm_t0C_WuD0a5VYZ3ECdg2HNmY",
        "description": "Overlooking the Mediterranean, The Alabaster Pavilion is a modernist masterpiece of white concrete and glass, with sunlight choreographed through every window at twilight.",
        "vision": "Designed by Atelier Cassar, this cliffside villa pairs sculptural forms with the rugged Côte d'Azur. Floor-to-ceiling glazing frames the bay; polished travertine floors carry the horizon inside.\n\nFrom the sunken salon to the suspended infinity pool, every threshold is a deliberate encounter with light.",
        "featured": True,
        "agent": "Julian Vane",
        "amenities": ["Infinity Pool", "Chef's Kitchen", "Wine Cellar", "Smart Home"],
        "features": [
            ("pool", "Infinity Lap Pool", "75-foot heated pool with saltwater filtration and panoramic ocean views."),
            ("restaurant", "Chef's Kitchen", "Dual islands, Gaggenau appliances, and a hidden butler's pantry."),
            ("local_fire_department", "Outdoor Fire Lounge", "Sunken seating area with a custom-built bronze fire pit."),
            ("health_and_safety", "Smart Sanctuary", "Full Crestron automation for lighting, climate, and biometric security."),
        ],
        "images": [
            "https://lh3.googleusercontent.com/aida-public/AB6AXuChFJUJ1vhVKx_IwV2MdNxN-UZ7MsZCXFYzY4z_fJmtkH9d6t0t37AIOZV3whPL2iwf30fVnTRQmzWzKM2obSlWynv-h5Obp1btiwloFF6QIdjzJfz3ZIvFzh44qh_szuZ_cYdnpfA9MWB9TNdc32GHh9tgr0R3Y4lCOLn4J6pKK-4ON8f_x3SVpGXdymXMkuVQ0GWj5xuMXUoWZTUQK1wwrEBCX6DJsQQr2zt10hZ2VDk_sb8zlObkgj_WNuiiMh1mPGUoPbbZvW8",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBxwJ7MH3yitInxKiDpVwC4-4XY_LFIKz9Byr1Zrt6-w3zLlt44uG4T-w8uj3p22dJTA64i8T0lrxO-feFkLjElEZeU0eucuiesdsigpHzXdO88tZaq0dA1tpjEsVnc8NJMJqjZ-y3zT2Zo2CLuY63StXkz-CT16Iir7dhtnRfgPEX5Y5SYMb7dwio0pvKt8AV82P4OyzFnSvTSQuAZeR_FaS68OtVGuRcLVcfvrzTwkXKUawcrMyjE2O-e2afQ1kxUc2FC15Wm8zk",
        ],
    },
    {
        "title": "Shadow & Timber Lodge",
        "location": ("Aspen", "United States"),
        "type": "Heritage Manor",
        "status": "active",
        "price": Decimal("12900000"),
        "bedrooms": 5,
        "bathrooms": 5,
        "square_feet": 8200,
        "garage_spaces": 3,
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuBu-548UV-FBAUngkphyKpwoT6M5aN-f7-FiOKyNUwXhG49URvgqp-wyv4NUbAeqjKu2lFsGu6sXU_z_frgTgINsosoCo78z31uUZCqpjgElCW-rFxZxJemqHcm6ne0kThTAA8nIaFLtMmOZ7ZMaIhCSzFG1tcoyGhmWsB4APEQUZWdeRtUZFlMUy__HhEig_lBFoNXVWWoKjx-qB8PjxqD4g4KlOdMnGbc0edacvhp0jZmTobiX3S46UQ2IwbKjBoDFH1O8OLiDt4",
        "description": "A brutalist concrete and reclaimed timber refuge carved into a mountain ridge, where snow-light plays across raw material and patinated bronze.",
        "vision": "Set against an Aspen alpine backdrop, Shadow & Timber is a study in contrast: monolithic walls meet century-old beams sourced from dismantled Wyoming barns.\n\nThe living room anchors a double-sided basalt hearth; wraparound decks integrate outdoor spas and an open-air sauna.",
        "featured": False,
        "agent": "Elena Thorne",
        "amenities": ["Private Gym", "Wine Cellar", "Home Theater"],
        "features": [],
        "images": [],
    },
    {
        "title": "Horizon Point Estate",
        "location": ("Malibu", "United States"),
        "type": "Coastal Estate",
        "status": "new",
        "price": Decimal("34000000"),
        "bedrooms": 7,
        "bathrooms": 9,
        "square_feet": 15000,
        "garage_spaces": 5,
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuCntvkKPO9vheLGNFOAM0bRa27Ga4C2oSsD4bF8JViJmX3W-9khlvwSoKIHWfIfTknxREAPigeKNO6m2PSTKcKIbO_WOqRiRkEcDxbt3sbmZpe3bJKOIidOEpif6wjXrpQb6N_zYarBVYb4R226iY6sqtyCODpP3OjLabj-CW6WECKgKXjzXYOVaqDJX-rHL67ytv4dvDJNuBTOvjSbJ9abW5R6zgoyIoDVRY7F-TNwsLdIuFuSn5yziLkKJ-Tfh3eEftEv_-IZeIE",
        "description": "Sleek contemporary waterfront estate with a 100-foot infinity pool framed against the Pacific.",
        "vision": "Horizon Point is a horizontal composition of cantilevered concrete and bronze-clad glass. Every room is oriented around the ocean; the main level dissolves into a suspended terrace above the surf.",
        "featured": True,
        "agent": "Marcus Sterling",
        "amenities": ["Infinity Pool", "Helipad", "Home Theater", "Smart Home"],
        "features": [
            ("pool", "Oceanfront Pool", "100-foot infinity edge with underwater lounge and glass wall."),
            ("flight", "Private Helipad", "Coastal-access pad cleared for VFR day operations."),
        ],
        "images": [],
    },
    {
        "title": "Villa di Smeraldo",
        "location": ("Siena", "Italy"),
        "type": "Historic Manor",
        "status": "exclusive",
        "price": Decimal("42000000"),
        "bedrooms": 12,
        "bathrooms": 14,
        "square_feet": 24000,
        "garage_spaces": 6,
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuDycMLd40P8AIhBuxxY82-JIeCJi3X9C5tOasB0gsuOJuWIIa-h6eCZkkoeI8LrPILlBQJs6XtK-misRoZkY-jA_znCpfO3eaH-rK4UaWdh-2OsEDkLk2Gq6e3ZwpL8j2oPealHtun3rt5mlQR9vd6RDLdwlEziNn3_TI1KXe1wiR2Eg-_eKEFH2okqH28xZe4Kmt2jIKHavkhBsL9rsvKck42iFf6qkgmW8wX2CtQNmqw4_IKCvGRvQAZEUKUC4-1IdvkaIleWVBQ",
        "description": "A stately Renaissance villa with cypress avenues and lavender gardens, sited on 120 hectares of Tuscan terroir.",
        "vision": "Restored frescoes and bespoke stonework carry the estate's four centuries of history, while discreetly embedded automation meets the demands of modern custodianship.",
        "featured": True,
        "agent": "Julian Vane",
        "amenities": ["Private Vineyard", "Wine Cellar", "Chef's Kitchen"],
        "features": [],
        "images": [],
    },
    {
        "title": "The Zenith Penthouse",
        "location": ("Manhattan", "United States"),
        "type": "Modern Penthouse",
        "status": "active",
        "price": Decimal("27500000"),
        "bedrooms": 3,
        "bathrooms": 4,
        "square_feet": 6500,
        "garage_spaces": 2,
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuBeaqd3wEBYz-qMTEVl1BoCnWQpsAUWsvJL0UUJaB04xdP_UfFxUMSkIMOyM-cy22lESIeMKAvXwpWnj53k3U4DoLbJ5ITVreID-We4xMw3bZbtpCTuXXQ2TkZeylas6Zt3kKm03g_BLdc6yWWxvEfdmGyv9ioOLQwMDj-8YvmLXxRTBnafGDK3jurBMu4k4wF8FLp8KZArz1WAwXjrQ93FPKP5xKu6lKJynpNLlSRn_1n1DYmb2Lng00FjktPe-luaw69b4T8HoPk",
        "description": "Floor-to-ceiling glass wraps the Zenith Penthouse, hovering 70 stories above Central Park with a private rooftop terrace.",
        "vision": "A 360-degree glass crown over Midtown. Interior surfaces by Studio Aplós—travertine, burled walnut, and brushed bronze—echo the editorial language of the building's architect.",
        "featured": False,
        "agent": "Sophia Aris",
        "amenities": ["Smart Home", "Home Theater", "Private Gym"],
        "features": [],
        "images": [],
    },
    {
        "title": "The Obsidian Sanctuary",
        "location": ("Joshua Tree", "United States"),
        "type": "Minimalist Loft",
        "status": "active",
        "price": Decimal("8800000"),
        "bedrooms": 4,
        "bathrooms": 3,
        "square_feet": 4200,
        "garage_spaces": 2,
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuBZE4alGM7JQxZnAp_XpB8R_rHGz1SC88Hplfq5qwvpxxaIxE68zK-A-JGN0bioDiJv4RuYKkwgNTz_f_ZsyVIrg_EP8_tzOi2HEFTEOaBMexS82KUyoox-VStMKHLPs1sTEbfsKgaQf49--1ibsclo3055FnyGZWAssDterSFKRI1CfHbd2aPYDkXfQviLEaWQ96AkmNnwlEe8bsb5LXhBMJa72p5cbD6zCMKp-KACEjn5VaS60cr8zMZ0hn5vbuIN3XvpYnYEVkc",
        "description": "Ultra-minimalist black glass house reflecting desert sunrise, dunes and Joshua Trees in the foreground.",
        "vision": "A meditation on stillness. Black anodized steel vanishes into the desert floor at dawn, and a subterranean pool reflects the Milky Way on clear nights.",
        "featured": False,
        "agent": "Elena Thorne",
        "amenities": ["Infinity Pool", "Smart Home"],
        "features": [],
        "images": [],
    },
    {
        "title": "Aurelian Estate",
        "location": ("Montecito", "United States"),
        "type": "Coastal Estate",
        "status": "exclusive",
        "price": Decimal("12450000"),
        "bedrooms": 6,
        "bathrooms": 8,
        "square_feet": 8400,
        "garage_spaces": 4,
        "address": "127 Zenith Terrace",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuB3kp_DuZNJO6Z-aRGmXGue-N1SZFN-Ot4zHuj4HSjKZpNsQ84O2dl5Ut2CcezcJ5Yof6dajzIo7TZXnaKITiCKd_HW0QPmRnSpYNO_yPl3kE4Sx4hAiqcKQ7cUipJYrR2IX7t15Ztx59izesY01T0bVG1XG7e70QcauqWdKe8azYSswP8MLcoa6Ozya7DbgP4j_hifFWyV2FQsTXMH2UNlwTWnEiiBN0iKQk-JnG9dGh4XYBtdnQTHNMJKf0gFAkABMffzm-d2ibI",
        "description": "Commanding a prestigious cliffside position, the Aurelian Estate is a masterwork of contemporary architecture that blurs the boundaries between indoor luxury and the wild beauty of the California coast.",
        "vision": "Commanding a prestigious cliffside position, the Aurelian Estate is a masterwork of contemporary architecture that blurs the boundaries between indoor luxury and the wild beauty of the California coast. Designed by the award-winning firm Aperture Arch, every angle of this residence is curated to frame the horizon.\n\nFrom the double-height gallery entrance to the subterranean wine cellar carved directly into the coastal stone, the property utilizes a palette of raw concrete, fluted bronze, and Italian travertine. This is not merely a home; it is a monolith of light and space.",
        "tagline": "Est. Mortgage: $62,000/mo",
        "featured": True,
        "agent": "Marcus Sterling",
        "amenities": ["Infinity Pool", "Chef's Kitchen", "Wine Cellar", "Smart Home"],
        "features": [
            ("pool", "Infinity Lap Pool", "75-foot heated pool with saltwater filtration and panoramic ocean views."),
            ("restaurant", "Chef's Kitchen", "Dual islands, Gaggenau appliances, and a hidden butler's pantry."),
            ("local_fire_department", "Outdoor Fire Lounge", "Sunken seating area with a custom-built bronze fire pit."),
            ("health_and_safety", "Smart Sanctuary", "Full Crestron automation for lighting, climate, and biometric security."),
        ],
        "images": [
            "https://lh3.googleusercontent.com/aida-public/AB6AXuChFJUJ1vhVKx_IwV2MdNxN-UZ7MsZCXFYzY4z_fJmtkH9d6t0t37AIOZV3whPL2iwf30fVnTRQmzWzKM2obSlWynv-h5Obp1btiwloFF6QIdjzJfz3ZIvFzh44qh_szuZ_cYdnpfA9MWB9TNdc32GHh9tgr0R3Y4lCOLn4J6pKK-4ON8f_x3SVpGXdymXMkuVQ0GWj5xuMXUoWZTUQK1wwrEBCX6DJsQQr2zt10hZ2VDk_sb8zlObkgj_WNuiiMh1mPGUoPbbZvW8",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBxwJ7MH3yitInxKiDpVwC4-4XY_LFIKz9Byr1Zrt6-w3zLlt44uG4T-w8uj3p22dJTA64i8T0lrxO-feFkLjElEZeU0eucuiesdsigpHzXdO88tZaq0dA1tpjEsVnc8NJMJqjZ-y3zT2Zo2CLuY63StXkz-CT16Iir7dhtnRfgPEX5Y5SYMb7dwio0pvKt8AV82P4OyzFnSvTSQuAZeR_FaS68OtVGuRcLVcfvrzTwkXKUawcrMyjE2O-e2afQ1kxUc2FC15Wm8zk",
        ],
    },
]

TESTIMONIALS = [
    {
        "quote": "The level of discretion and curation provided by Aperture is unparalleled. They understood my aesthetic requirements before I even voiced them.",
        "author": "Julian Thorne",
        "role": "Venture Capitalist",
        "photo_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBwg51Zw-3AhqFEPNkVLvfO3cIai-8ZiVk-h28zSnGX94tqjAaZL7g97MQ8_Uak5xKDT17EcVPtwtNaOdMYAdIXlNlUF7R-xGUwA95uumdC6AVjD-lVwwg8sABl9BwX2OI5aR2_ZrEaLFHfIOjDP0EEwAv7lQsRTc3KYOfVPqEIg_1ZvdBaMEKvIvnKJdGJz7CvmBilPdVh6YBxjPb0tTBrq3TsVp8ZxFnwzs4OuJ7WkttBlsuzBCxKlwi1odzFbv2n4sLOaSBeOr8",
        "order": 1,
    },
    {
        "quote": "They don't just sell houses. They find settings for your future. Our new estate in Provence is more than a home, it's a masterpiece.",
        "author": "Elena Rossi",
        "role": "Creative Director",
        "photo_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCO2b2h6t6xruo9jTCVMSXRQExghHnHOVVrpl-AzpN_3EAZftmDh2gqNxzvYg6BP4Iuo_VM0Z1ZUlKOVk6bPRk_3hZ-5V8vRe8bnAj9Iq_smOAlNyQC9kAh2xYb4_qOCt4IZcqZibyhC5OZN2mVJQ19BfHPW5yklmRr2PJCHyv4PelTH0OQo70Yc0LYiXuPdJwqgRORqm4OWFAHp-ut72Ud_h6yZMqipECGpge9-7Nggi_pd4AAi_bJ8x85FjR7hQ_NdW9uZjK5PKo",
        "order": 2,
    },
]


class Command(BaseCommand):
    help = "Seed the database with demo content from the Aperture wireframes."

    @transaction.atomic
    def handle(self, *args, **options):
        SiteSettings.load()

        loc_map = {}
        for city, region, country in LOCATIONS:
            loc, _ = Location.objects.get_or_create(
                city=city, country=country, defaults={"region": region}
            )
            loc_map[(city, country)] = loc

        type_map = {}
        for name in TYPES:
            t, _ = PropertyType.objects.get_or_create(name=name)
            type_map[name] = t

        amenity_map = {}
        for name, icon in AMENITIES:
            a, _ = Amenity.objects.get_or_create(name=name, defaults={"icon": icon})
            amenity_map[name] = a

        agent_map = {}
        for data in AGENTS:
            agent, _ = Agent.objects.update_or_create(name=data["name"], defaults=data)
            agent_map[data["name"]] = agent

        for data in PROPERTIES:
            loc = loc_map[data["location"]]
            ptype = type_map[data["type"]]
            agent = agent_map.get(data.get("agent"))
            prop, _ = Property.objects.update_or_create(
                title=data["title"],
                defaults={
                    "location": loc,
                    "property_type": ptype,
                    "agent": agent,
                    "status": data["status"],
                    "price": data["price"],
                    "bedrooms": data["bedrooms"],
                    "bathrooms": data["bathrooms"],
                    "square_feet": data["square_feet"],
                    "garage_spaces": data["garage_spaces"],
                    "address": data.get("address", ""),
                    "tagline": data.get("tagline", ""),
                    "description": data["description"],
                    "vision": data.get("vision", ""),
                    "cover_image_url": data.get("cover", ""),
                    "featured": data.get("featured", False),
                    "is_published": True,
                },
            )
            prop.amenities.set([amenity_map[n] for n in data.get("amenities", [])])

            prop.features.all().delete()
            for i, (icon, title, desc) in enumerate(data.get("features", [])):
                PropertyFeature.objects.create(
                    property=prop, icon=icon, title=title, description=desc, order=i
                )

            prop.images.all().delete()
            for i, url in enumerate(data.get("images", [])):
                PropertyImage.objects.create(
                    property=prop, image_url=url, order=i, alt=prop.title
                )

        for data in TESTIMONIALS:
            Testimonial.objects.update_or_create(author=data["author"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Seed complete."))
