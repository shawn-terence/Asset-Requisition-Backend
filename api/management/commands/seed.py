from django.core.management.base import BaseCommand
from api.models import Asset, Request
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Delete existing data
        self.stdout.write("Deleting old data...")
        Request.objects.all().delete()
        Asset.objects.all().delete()
        User.objects.all().delete()

        # Create users
        self.stdout.write("Creating new users...")
        superadmin = User.objects.create_superuser(
            email="superadmin@example.com",
            first_name="Super",
            last_name="Admin",
            phone_number="1234567890",
            department="Management",
            role="superadmin",
            password="password123",
        )

        admin1 = User.objects.create_user(
            email="admin1@example.com",
            first_name="Admin",
            last_name="One",
            phone_number="1234567891",
            department="IT",
            role="admin",
            password="password123",
        )

        admin2 = User.objects.create_user(
            email="johndoe@example.com",
            first_name="John",
            last_name="Two",
            phone_number="1234567892",
            department="HR",
            role="admin",
            password="password123",
        )

        employee1 = User.objects.create_user(
            email="pete@example.com",
            first_name="Pete",
            last_name="One",
            phone_number="1234567893",
            department="Finance",
            role="employee",
            password="password123",
        )

        employee2 = User.objects.create_user(
            email="employee2@example.com",
            first_name="Employee",
            last_name="Two",
            phone_number="1234567894",
            department="Sales",
            role="employee",
            password="password123",
        )

        employee3 = User.objects.create_user(
            email="employee3@example.com",
            first_name="Employee",
            last_name="Three",
            phone_number="1234567895",
            department="Support",
            role="employee",
            password="password123",
        )

        employee4 = User.objects.create_user(
            email="employee4@example.com",
            first_name="Employee",
            last_name="Four",
            phone_number="1234567896",
            department="Development",
            role="employee",
            password="password123",
        )

        # Create assets
        self.stdout.write("Creating new assets...")
        assets = [
            {
                "name": "Laptop",
                "description": "Intel Core i7 processor, 16GB RAM, 512GB SSD, 15.6-inch Full HD display",
                "category": "Electronics",
                "serial_number": "SN123456",
                "tag": "IT",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632498/open-laptop_144627-12148_psdxwk.jpg",
            },
            {
                "name": "Projector",
                "description": "4000 lumens brightness, 1080p resolution, 1.2-1.5 zoom lens",
                "category": "Electronics",
                "serial_number": "SN123457",
                "tag": "AV",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632532/projector_enpi3j.avif",
            },
            {
                "name": "Desk Chair",
                "description": "Adjustable height (18-22 inches), lumbar support, breathable mesh back",
                "category": "Furniture",
                "serial_number": "SN123458",
                "tag": "Office",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632485/office-chair-still-life_23-2151149132_keg49b.jpg",
            },
            {
                "name": "Monitor",
                "description": "32-inch 4K UHD, 3840x2160 resolution, HDR support, 60Hz refresh rate",
                "category": "Electronics",
                "serial_number": "SN123459",
                "tag": "IT",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632280/3cb2fd73d55747db5675a293dc8fcba1-qm24dfi-foto01_tzy8cp.jpg",
            },
            {
                "name": "Keyboard",
                "description": "Mechanical switches, RGB backlighting, USB connectivity, 104-key layout",
                "category": "Electronics",
                "serial_number": "SN123460",
                "tag": "IT",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632562/wireless-mouse-keyboard_1260-15_jj31su.jpg",
            },
            {
                "name": "Desk",
                "description": "Large wooden desk, dimensions 60x30 inches, with cable management system",
                "category": "Furniture",
                "serial_number": "SN123461",
                "tag": "Office",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632472/desk_ylkwxv.webp",
            },
            {
                "name": "Office Chair",
                "description": "Ergonomic office chair, adjustable seat height (16-21 inches), swivel base",
                "category": "Furniture",
                "serial_number": "SN123462",
                "tag": "Office",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632462/chair_oip9la.jpg",
            },
            {
                "name": "Printer",
                "description": "Laser printer, print speed 35 ppm, automatic duplex printing, USB and Wi-Fi",
                "category": "Electronics",
                "serial_number": "SN123463",
                "tag": "IT",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632516/printer-with-white-sheets_1232-570_l52ui5.jpg",
            },
            {
                "name": "Tablet",
                "description": "10.5-inch display, 128GB storage, 8GB RAM, A12 Bionic chip",
                "category": "Electronics",
                "serial_number": "SN123464",
                "tag": "IT",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632546/tablet-mockup_1017-7628_zxncfy.jpg",
            },
            {
                "name": "Headphones",
                "description": "Over-ear noise-cancelling headphones, 20 hours battery life, Bluetooth 5.0",
                "category": "Electronics",
                "serial_number": "SN123465",
                "tag": "AV",
                "status": True,
                "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1737632442/black-headphones-digital-device_53876-96805_q1a8km.jpg",
            },



            {
                    "name": "Cordless Drill",
                    "description": "20V MAX lithium-ion, 1/2-inch chuck, 2-speed transmission (0-550/0-2000 RPM)",
                    "category": "Tools",
                    "serial_number": "SN123466",
                    "tag": "Maintenance",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645147/drill_dbut66.jpg"
                },
                {
                    "name": "External Hard Drive",
                    "description": "4TB USB 3.0, 7200 RPM, hardware encryption, shock-resistant casing",
                    "category": "Electronics",
                    "serial_number": "SN123467",
                    "tag": "IT",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645330/harddrive_nup3yg.jpg"
                },
                {
                    "name": "Whiteboard",
                    "description": "4x6 feet magnetic dry-erase surface, aluminum frame, marker tray",
                    "category": "Furniture",
                    "serial_number": "SN123468",
                    "tag": "Office",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645175/whiteboard_qhnmlg.jpg"
                },
                {
                    "name": "Wi-Fi Router",
                    "description": "AX6000 dual-band, 8-stream, 4x4 MU-MIMO, OFDMA technology",
                    "category": "Electronics",
                    "serial_number": "SN123469",
                    "tag": "Networking",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645258/router_iyqy5l.jpg"
                },
                {
                    "name": "Fire Extinguisher",
                    "description": "10-pound ABC dry chemical, 15-20 second discharge time, UL rated",
                    "category": "Safety Equipment",
                    "serial_number": "SN123470",
                    "tag": "Facilities",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645155/extinguish_i8v1u4.jpg"
                },
                {
                    "name": "First Aid Kit",
                    "description": "200-piece OSHA compliant, includes burn gel, CPR mask, trauma pad",
                    "category": "Safety Equipment",
                    "serial_number": "SN123471",
                    "tag": "Facilities",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645082/aid_xexueu.jpg"
                },
                {
                    "name": "Conference Phone",
                    "description": "360° voice capture, Bluetooth 5.1, HD audio, 12-hour battery life",
                    "category": "Electronics",
                    "serial_number": "SN123472",
                    "tag": "AV",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645136/CP-8845-K9-Cisco-8800-IP-Phone_wrm76w.webp"
                },
                {
                    "name": "Shredder",
                    "description": "Cross-cut 18-sheet capacity, 0.16x0.47 inch particle size, 7-gallon bin",
                    "category": "Office Equipment",
                    "serial_number": "SN123473",
                    "tag": "Admin",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645228/shredder_k6odmw.webp"
                },
                {
                    "name": "3D Printer",
                    "description": "FDM technology, 8.7x7.9x7.9 inch build volume, 0.05mm layer resolution",
                    "category": "Electronics",
                    "serial_number": "SN123474",
                    "tag": "IT",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645299/printer3d_fw1oql.jpg"
                },
                {
                    "name": "Barcode Scanner",
                    "description": "2D imager, USB/Bluetooth connectivity, 100 scans/sec, IP54 rated",
                    "category": "Electronics",
                    "serial_number": "SN123475",
                    "tag": "IT",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645125/barcode_pt28ap.jpg"
                },
                {
                    "name": "Air Purifier",
                    "description": "HEPA filter + activated carbon, 1500 sq ft coverage, 55 dB noise level",
                    "category": "Appliances",
                    "serial_number": "SN123476",
                    "tag": "Facilities",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645274/purifier_e4ldbh.jpg"
                },
                {
                    "name": "Tool Kit",
                    "description": "192-piece mechanics set, SAE/metric, chrome vanadium steel",
                    "category": "Tools",
                    "serial_number": "SN123477",
                    "tag": "Maintenance",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645198/toolkit_nj7x0b.jpg"
                },
                {
                    "name": "Server Rack",
                    "description": "42U height, 19-inch width, perforated doors, cooling fans",
                    "category": "Electronics",
                    "serial_number": "SN123478",
                    "tag": "Networking",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645241/server_qhguvy.webp"
                },
                {
                    "name": "Stapler",
                    "description": "Heavy-duty 20-sheet capacity, full strip, chrome steel construction",
                    "category": "Office Supplies",
                    "serial_number": "SN123481",
                    "tag": "Admin",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645216/stapler_fbvsnr.jpg"
                },
                {
                    "name": "UPS",
                    "description": "1500VA/900W, 6 outlets, LCD display, AVR, 5-8 minute runtime",
                    "category": "Electronics",
                    "serial_number": "SN123482",
                    "tag": "IT",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645185/ups_tv14hc.webp"
                },
                {
                    "name": "Graphic Tablet",
                    "description": "10x6 inch active area, 8192 pressure levels, tilt recognition",
                    "category": "Electronics",
                    "serial_number": "SN123483",
                    "tag": "IT",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645344/graphic_hdxejs.jpg"
                },
                {
                    "name": "Portable Heater",
                    "description": "1500W ceramic heater, thermostat control, tip-over protection",
                    "category": "Appliances",
                    "serial_number": "SN123485",
                    "tag": "Facilities",
                    "status": True,
                    "link": "https://res.cloudinary.com/dcqpver8i/image/upload/v1738645317/heater_vomlrh.jpg"
                }
        ]

        for asset_data in assets:
            Asset.objects.create(**asset_data)
        # Create requests and set asset status to False when requested
        self.stdout.write("Creating new requests and updating asset status...")

        # Employee1 requests asset1 (status becomes False)
        asset1 = Asset.objects.get(serial_number="SN123456")
        Request.objects.create(
            asset=asset1,
            employee=employee1,
            status="pending",
            notes="Need this for remote work.",
        )
        asset1.status = False
        asset1.save()

        # Employee2 requests asset2 (status becomes False)
        asset2 = Asset.objects.get(serial_number="SN123457")
        Request.objects.create(
            asset=asset2,
            employee=employee2,
            status="pending",
            notes="Required for a presentation.",
        )
        asset2.status = False
        asset2.save()

        # Employee3 requests asset3 (status becomes False)
        asset3 = Asset.objects.get(serial_number="SN123458")
        Request.objects.create(
            asset=asset3,
            employee=employee3,
            status="pending",
            notes="Need a comfortable chair for long hours.",
        )
        asset3.status = False
        asset3.save()

        # Admin1 rejects a request
        rejected_request = Request.objects.create(
            asset=asset3,
            employee=employee4,
            status="rejected",
            return_status="rejected",
            notes="This asset is required for a higher-priority project.",
        )
        asset3.status = True  # Set asset status back to True
        asset3.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully seeded the database with users, assets, and requests")
        )