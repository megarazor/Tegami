from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

QUERY_GENDER_CHOICES= [
    (-1, 'Any'),
    (0, 'Female'),
    (1, 'Male'),
    (2, 'Other')
]

QUERY_COUNTRY_CHOICES= [
    ('--', 'Any'),
    ('AF', 'Afghanistan'),
    ('AX', 'Aland Islands'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BQ', 'Bonaire, Sint Eustatius and Saba'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos (Keeling) Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo, The Democratic Republic of'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Cote d\'Ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CW', 'Curaçao'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czechia'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French Southern Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GG', 'Guernsey'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HM', 'Heard and Mc Donald Islands'),
    ('VA', 'Holy See (Vatican City State)'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran Islamic Republic of'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IM', 'Isle of Man'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JE', 'Jersey'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea Democratic People\'s Republic of'),
    ('KR', 'Korea, Republic of'),
    ('XK', 'Kosovo (temporary code)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Lao, People\'s Democratic Republic'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libyan Arab Jamahiriya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macao'),
    ('MK', 'Macedonia, The Former Yugoslav Republic Of'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia, Federated States of'),
    ('MD', 'Moldova, Republic of'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('AN', 'Netherlands Antilles'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PS', 'Palestinian Territory Occupied'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RS', 'Republic of Serbia'),
    ('RE', 'Reunion'),
    ('RO', 'Romania'),
    ('RU', 'Russia Federation'),
    ('RW', 'Rwanda'),
    ('BL', 'Saint Barthélemy'),
    ('SH', 'Saint Helena'),
    ('KN', 'Saint Kitts & Nevis'),
    ('LC', 'Saint Lucia'),
    ('MF', 'Saint Martin'),
    ('PM', 'Saint Pierre and Miquelon'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome and Principe'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('CS', 'Serbia and Montenegro'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SX', 'Sint Maarten'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('GS', 'South Georgia & The South Sandwich Islands'),
    ('SS', 'South Sudan'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SJ', 'Svalbard and Jan Mayen'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan, Province of China'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania, United Republic of'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('XT', 'Turkish Rep N Cyprus (temporary code)'),
    ('TM', 'Turkmenistan'),
    ('TC', 'Turks and Caicos Islands'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('GB', 'United Kingdom'),
    ('US', 'United States'),
    ('UM', 'United States Minor Outlying Islands'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela'),
    ('VN', 'Vietnam'),
    ('VG', 'Virgin Islands, British'),
    ('VI', 'Virgin Islands, U.S.'),
    ('WF', 'Wallis and Futuna'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe')
]

QUERY_LANGUAGE_CHOICES= [
    ('--', 'Any'),
    ('aa', 'Afar'),
    ('ab', 'Abkhazian'),
    ('ae', 'Avestan'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('am', 'Amharic'),
    ('an', 'Aragonese'),
    ('ar', 'Arabic'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('ba', 'Bashkir'),
    ('be', 'Belarusian'),
    ('bg', 'Bulgarian'),
    ('bh', 'Bihari languages'),
    ('bi', 'Bislama'),
    ('bm', 'Bambara'),
    ('bn', 'Bengali'),
    ('bo', 'Tibetan'),
    ('br', 'Breton'),
    ('bs', 'Bosnian'),
    ('ca', 'Catalan; Valencian'),
    ('ce', 'Chechen'),
    ('ch', 'Chamorro'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('cs', 'Czech'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cv', 'Chuvash'),
    ('cy', 'Welsh'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dv', 'Divehi; Dhivehi; Maldivian'),
    ('dz', 'Dzongkha'),
    ('ee', 'Ewe'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('es', 'Spanish; Castilian'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('fa', 'Persian'),
    ('ff', 'Fulah'),
    ('fi', 'Finnish'),
    ('fj', 'Fijian'),
    ('fo', 'Faroese'),
    ('fr', 'French'),
    ('fy', 'Western Frisian'),
    ('ga', 'Irish'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('gl', 'Galician'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('gv', 'Manx'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hr', 'Croatian'),
    ('ht', 'Haitian; Haitian Creole'),
    ('hu', 'Hungarian'),
    ('hy', 'Armenian'),
    ('hz', 'Herero'),
    ('ia', 'Interlingua (International Auxiliary Language Association)'),
    ('id', 'Indonesian'),
    ('ie', 'Interlingue; Occidental'),
    ('ig', 'Igbo'),
    ('ii', 'Sichuan Yi; Nuosu'),
    ('ik', 'Inupiaq'),
    ('io', 'Ido'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('iu', 'Inuktitut'),
    ('ja', 'Japanese'),
    ('jv', 'Javanese'),
    ('ka', 'Georgian'),
    ('kg', 'Kongo'),
    ('ki', 'Kikuyu; Gikuyu'),
    ('kj', 'Kuanyama; Kwanyama'),
    ('kk', 'Kazakh'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('km', 'Central Khmer'),
    ('kn', 'Kannada'),
    ('ko', 'Korean'),
    ('kr', 'Kanuri'),
    ('ks', 'Kashmiri'),
    ('ku', 'Kurdish'),
    ('kv', 'Komi'),
    ('kw', 'Cornish'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('la', 'Latin'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('lg', 'Ganda'),
    ('li', 'Limburgan; Limburger; Limburgish'),
    ('ln', 'Lingala'),
    ('lo', 'Lao'),
    ('lt', 'Lithuanian'),
    ('lu', 'Luba-Katanga'),
    ('lv', 'Latvian'),
    ('mg', 'Malagasy'),
    ('mh', 'Marshallese'),
    ('mi', 'Maori'),
    ('mk', 'Macedonian'),
    ('ml', 'Malayalam'),
    ('mn', 'Mongolian'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('mt', 'Maltese'),
    ('my', 'Burmese'),
    ('na', 'Nauru'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'),
    ('nd', 'Ndebele, North; North Ndebele'),
    ('ne', 'Nepali'),
    ('ng', 'Ndonga'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('no', 'Norwegian'),
    ('nr', 'Ndebele, South; South Ndebele'),
    ('nv', 'Navajo; Navaho'),
    ('ny', 'Chichewa; Chewa; Nyanja'),
    ('oc', 'Occitan (post 1500)'),
    ('oj', 'Ojibwa'),
    ('om', 'Oromo'),
    ('or', 'Oriya'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('ps', 'Pushto; Pashto'),
    ('pt', 'Portuguese'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('rn', 'Rundi'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ru', 'Russian'),
    ('rw', 'Kinyarwanda'),
    ('sa', 'Sanskrit'),
    ('sc', 'Sardinian'),
    ('sd', 'Sindhi'),
    ('se', 'Northern Sami'),
    ('sg', 'Sango'),
    ('si', 'Sinhala; Sinhalese'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('sm', 'Samoan'),
    ('sn', 'Shona'),
    ('so', 'Somali'),
    ('sq', 'Albanian'),
    ('sr', 'Serbian'),
    ('ss', 'Swati'),
    ('st', 'Sotho, Southern'),
    ('su', 'Sundanese'),
    ('sv', 'Swedish'),
    ('sw', 'Swahili'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('th', 'Thai'),
    ('ti', 'Tigrinya'),
    ('tk', 'Turkmen'),
    ('tl', 'Tagalog'),
    ('tn', 'Tswana'),
    ('to', 'Tonga (Tonga Islands)'),
    ('tr', 'Turkish'),
    ('ts', 'Tsonga'),
    ('tt', 'Tatar'),
    ('tw', 'Twi'),
    ('ty', 'Tahitian'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('vo', 'Volapük'),
    ('wa', 'Walloon'),
    ('wo', 'Wolof'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu')
]

QUERY_AGE_CHOICES= [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
    (12, '12'),
    (13, '13'),
    (14, '14'),
    (15, '15'),
    (16, '16'),
    (17, '17'),
    (18, '18'),
    (19, '19'),
    (20, '20'),
    (21, '21'),
    (22, '22'),
    (23, '23'),
    (24, '24'),
    (25, '25'),
    (26, '26'),
    (27, '27'),
    (28, '28'),
    (29, '29'),
    (30, '30'),
    (31, '31'),
    (32, '32'),
    (33, '33'),
    (34, '34'),
    (35, '35'),
    (36, '36'),
    (37, '37'),
    (38, '38'),
    (39, '39'),
    (40, '40'),
    (41, '41'),
    (42, '42'),
    (43, '43'),
    (44, '44'),
    (45, '45'),
    (46, '46'),
    (47, '47'),
    (48, '48'),
    (49, '49'),
    (50, '50'),
    (51, '51'),
    (52, '52'),
    (53, '53'),
    (54, '54'),
    (55, '55'),
    (56, '56'),
    (57, '57'),
    (58, '58'),
    (59, '59'),
    (60, '60'),
    (61, '61'),
    (62, '62'),
    (63, '63'),
    (64, '64'),
    (65, '65'),
    (66, '66'),
    (67, '67'),
    (68, '68'),
    (69, '69'),
    (70, '70'),
    (71, '71'),
    (72, '72'),
    (73, '73'),
    (74, '74'),
    (75, '75'),
    (76, '76'),
    (77, '77'),
    (78, '78'),
    (79, '79'),
    (80, '80'),
    (81, '81'),
    (82, '82'),
    (83, '83'),
    (84, '84'),
    (85, '85'),
    (86, '86'),
    (87, '87'),
    (88, '88'),
    (89, '89'),
    (90, '90'),
    (91, '91'),
    (92, '92'),
    (93, '93'),
    (94, '94'),
    (95, '95'),
    (96, '96'),
    (97, '97'),
    (98, '98'),
    (99, '99'),
    (100, '100'),
    (101, '101'),
    (102, '102'),
    (103, '103'),
    (104, '104'),
    (105, '105'),
    (106, '106'),
    (107, '107'),
    (108, '108'),
    (109, '109'),
    (110, '110'),
    (111, '111'),
    (112, '112'),
    (113, '113'),
    (114, '114'),
    (115, '115'),
    (116, '116'),
    (117, '117'),
    (118, '118'),
    (119, '119'),
    (120, '120'),
    (121, '121'),
    (122, '122'),
    (123, '123'),
    (124, '124'),
    (125, '125'),
    (126, '126'),
    (127, '127'),
    (128, '128'),
    (129, '129'),
    (130, '130'),
    (131, '131'),
    (132, '132'),
    (133, '133'),
    (134, '134'),
    (135, '135'),
    (136, '136'),
    (137, '137'),
    (138, '138'),
    (139, '139'),
    (140, '140'),
    (141, '141'),
    (142, '142'),
    (143, '143'),
    (144, '144'),
    (145, '145'),
    (146, '146'),
    (147, '147'),
    (148, '148'),
    (149, '149'),
    (150, '150'),
]

class MatchQueryForm(forms.Form):
    country= forms.ChoiceField(label='Country', choices=QUERY_COUNTRY_CHOICES)
    gender= forms.ChoiceField(label='Gender', choices=QUERY_GENDER_CHOICES)
    min_age= forms.ChoiceField(label='From the age of', choices=QUERY_AGE_CHOICES)
    max_age= forms.ChoiceField(label='to', choices=QUERY_AGE_CHOICES)
    language1= forms.ChoiceField(label='Language 1', choices=QUERY_LANGUAGE_CHOICES)
    language2= forms.ChoiceField(label='Language 2', choices=QUERY_LANGUAGE_CHOICES)
    language3= forms.ChoiceField(label='Language 3', choices=QUERY_LANGUAGE_CHOICES)
    language4= forms.ChoiceField(label='Language 4', choices=QUERY_LANGUAGE_CHOICES)
    language5= forms.ChoiceField(label='Language 5', choices=QUERY_LANGUAGE_CHOICES)