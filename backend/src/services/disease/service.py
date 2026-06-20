CROPS = {
    "hi": [
        {"id": "tomato", "name": "टमाटर (Tomato)"},
        {"id": "wheat", "name": "गेहूं (Wheat)"},
        {"id": "potato", "name": "आलू (Potato)"},
        {"id": "chilli", "name": "मिर्च (Chilli)"},
        {"id": "paddy", "name": "धान (Paddy)"},
    ],
    "en": [
        {"id": "tomato", "name": "Tomato"},
        {"id": "wheat", "name": "Wheat"},
        {"id": "potato", "name": "Potato"},
        {"id": "chilli", "name": "Chilli"},
        {"id": "paddy", "name": "Paddy"},
    ],
    "ta": [
        {"id": "tomato", "name": "தக்காளி (Tomato)"},
        {"id": "wheat", "name": "கோதுமை (Wheat)"},
        {"id": "potato", "name": "உருளைக்கிழங்கு (Potato)"},
        {"id": "chilli", "name": "மிளகாய் (Chilli)"},
        {"id": "paddy", "name": "நெல் (Paddy)"},
    ],
    "te": [
        {"id": "tomato", "name": "టమోటా (Tomato)"},
        {"id": "wheat", "name": "గోధుమ (Wheat)"},
        {"id": "potato", "name": "బంగాళాదుంప (Potato)"},
        {"id": "chilli", "name": "మిరపకాయ (Chilli)"},
        {"id": "paddy", "name": "వరి (Paddy)"},
    ],
    "mr": [
        {"id": "tomato", "name": "टोमॅटो (Tomato)"},
        {"id": "wheat", "name": "गहू (Wheat)"},
        {"id": "potato", "name": "बटाटा (Potato)"},
        {"id": "chilli", "name": "मिरची (Chilli)"},
        {"id": "paddy", "name": "भात (Paddy)"},
    ],
}

SYMPTOMS = {
    "tomato": {
        "hi": {
            "parts": [
                {"id": "leaves", "name": "पत्तियां (Leaves)"},
                {"id": "fruit", "name": "फल (Fruit)"},
                {"id": "stem", "name": "तना (Stem)"},
            ],
            "observations": [
                {"id": "spots", "name": "काले/भूरे धब्बे (Spots)"},
                {"id": "yellowing", "name": "पत्तियों का पीला होना (Yellowing)"},
                {"id": "rot", "name": "फल का सड़ना (Fruit Rot)"},
            ],
        },
        "en": {
            "parts": [
                {"id": "leaves", "name": "Leaves"},
                {"id": "fruit", "name": "Fruit"},
                {"id": "stem", "name": "Stem"},
            ],
            "observations": [
                {"id": "spots", "name": "Black/Brown spots"},
                {"id": "yellowing", "name": "Yellowing of leaves"},
                {"id": "rot", "name": "Fruit Rotting"},
            ],
        },
        "ta": {
            "parts": [
                {"id": "leaves", "name": "இலைகள் (Leaves)"},
                {"id": "fruit", "name": "பழம் (Fruit)"},
                {"id": "stem", "name": "தண்டு (Stem)"},
            ],
            "observations": [
                {"id": "spots", "name": "கருப்பு/பழுப்பு நிற புள்ளிகள் (Spots)"},
                {"id": "yellowing", "name": "இலை மஞ்சள் நிறமாதல் (Yellowing)"},
                {"id": "rot", "name": "பழம் அழுகுதல் (Fruit Rot)"},
            ],
        },
        "te": {
            "parts": [
                {"id": "leaves", "name": "ఆకులు (Leaves)"},
                {"id": "fruit", "name": "పండు (Fruit)"},
                {"id": "stem", "name": "కాండం (Stem)"},
            ],
            "observations": [
                {"id": "spots", "name": "నల్లటి/గోధుమ రంగు మచ్చలు (Spots)"},
                {"id": "yellowing", "name": "ఆకులు పసుపు రంగులోకి మారడం (Yellowing)"},
                {"id": "rot", "name": "పండు కుళ్ళిపోవడం (Fruit Rot)"},
            ],
        },
        "mr": {
            "parts": [
                {"id": "leaves", "name": "पाने (Leaves)"},
                {"id": "fruit", "name": "फळ (Fruit)"},
                {"id": "stem", "name": "खोड (Stem)"},
            ],
            "observations": [
                {"id": "spots", "name": "काळे/तपकिरी ठिपके (Spots)"},
                {"id": "yellowing", "name": "पाने पिवळी पडणे (Yellowing)"},
                {"id": "rot", "name": "फळ सडणे (Fruit Rot)"},
            ],
        },
    },
    "wheat": {
        "hi": {
            "parts": [
                {"id": "leaves", "name": "पत्तियां (Leaves)"},
                {"id": "fruit", "name": "दाना/बाली (Grain/Ear)"},
            ],
            "observations": [
                {"id": "yellowing", "name": "पत्तियों का पीला पड़ना (Yellowing)"},
                {"id": "rust", "name": "रस्ट/भूरा धब्बा पाउडर (Rust/Brown spots)"},
            ],
        },
        "en": {
            "parts": [
                {"id": "leaves", "name": "Leaves"},
                {"id": "fruit", "name": "Grain/Ear"},
            ],
            "observations": [
                {"id": "yellowing", "name": "Yellowing of leaves"},
                {"id": "rust", "name": "Rust/Brown powder spots"},
            ],
        },
        "ta": {
            "parts": [
                {"id": "leaves", "name": "இலைகள் (Leaves)"},
                {"id": "fruit", "name": "கதிர் (Grain/Ear)"},
            ],
            "observations": [
                {"id": "yellowing", "name": "மஞ்சள் நிறமாதல் (Yellowing)"},
                {"id": "rust", "name": "துரு நோய் (Rust)"},
            ],
        },
        "te": {
            "parts": [
                {"id": "leaves", "name": "ఆకులు (Leaves)"},
                {"id": "fruit", "name": "గింజ/కంకి (Grain/Ear)"},
            ],
            "observations": [
                {"id": "yellowing", "name": "ఆకులు పసుపు రంగులోకి మారడం (Yellowing)"},
                {"id": "rust", "name": "తుప్పు తెగులు (Rust)"},
            ],
        },
        "mr": {
            "parts": [
                {"id": "leaves", "name": "पाने (Leaves)"},
                {"id": "fruit", "name": "कणिस (Grain/Ear)"},
            ],
            "observations": [
                {"id": "yellowing", "name": "पाने पिवळी पडणे (Yellowing)"},
                {"id": "rust", "name": "तांबेरा रोग (Rust)"},
            ],
        },
    },
    "potato": {
        "hi": {
            "parts": [
                {"id": "leaves", "name": "पत्तियां (Leaves)"},
                {"id": "tuber", "name": "आलू/कंद (Tuber)"},
            ],
            "observations": [
                {"id": "blight", "name": "झुलसा रोग/धब्बे (Blight/Spots)"},
                {"id": "rot", "name": "कंद का सड़ना (Tuber Rot)"},
            ],
        },
        "en": {
            "parts": [
                {"id": "leaves", "name": "Leaves"},
                {"id": "tuber", "name": "Tuber"},
            ],
            "observations": [
                {"id": "blight", "name": "Blight spots"},
                {"id": "rot", "name": "Tuber rotting"},
            ],
        },
        "ta": {
            "parts": [
                {"id": "leaves", "name": "இலைகள் (Leaves)"},
                {"id": "tuber", "name": "கிழங்கு (Tuber)"},
            ],
            "observations": [
                {"id": "blight", "name": "இலைக்கருகல் நோய் (Blight)"},
                {"id": "rot", "name": "கிழங்கு அழுகல் (Tuber Rot)"},
            ],
        },
        "te": {
            "parts": [
                {"id": "leaves", "name": "ఆకులు (Leaves)"},
                {"id": "tuber", "name": "దుంప (Tuber)"},
            ],
            "observations": [
                {"id": "blight", "name": "మాడు తెగులు (Blight)"},
                {"id": "rot", "name": "దుంప కుళ్ళిపోవడం (Tuber Rot)"},
            ],
        },
        "mr": {
            "parts": [
                {"id": "leaves", "name": "पाने (Leaves)"},
                {"id": "tuber", "name": "बटाटा कंद (Tuber)"},
            ],
            "observations": [
                {"id": "blight", "name": "करपा रोग (Blight)"},
                {"id": "rot", "name": "कंद सडणे (Tuber Rot)"},
            ],
        },
    },
    "chilli": {
        "hi": {
            "parts": [
                {"id": "leaves", "name": "पत्तियां (Leaves)"},
                {"id": "fruit", "name": "मिर्च फल (Fruit)"},
            ],
            "observations": [
                {"id": "curl", "name": "पत्ती मुड़ना (Leaf Curl)"},
                {"id": "spots", "name": "फल पर धब्बे/सड़न (Fruit Spots/Rot)"},
            ],
        },
        "en": {
            "parts": [
                {"id": "leaves", "name": "Leaves"},
                {"id": "fruit", "name": "Fruit"},
            ],
            "observations": [
                {"id": "curl", "name": "Leaf Curl (Murraiah)"},
                {"id": "spots", "name": "Fruit spots or rotting"},
            ],
        },
        "ta": {
            "parts": [
                {"id": "leaves", "name": "இலைகள் (Leaves)"},
                {"id": "fruit", "name": "மிளகாய் பழம் (Fruit)"},
            ],
            "observations": [
                {"id": "curl", "name": "இலைச்சுருட்டல் நோய் (Leaf Curl)"},
                {"id": "spots", "name": "மிளகாய் அழுகல் (Fruit Spots/Rot)"},
            ],
        },
        "te": {
            "parts": [
                {"id": "leaves", "name": "ఆకులు (Leaves)"},
                {"id": "fruit", "name": "మిరప కాయ (Fruit)"},
            ],
            "observations": [
                {"id": "curl", "name": "ఆకు ముడత తెగులు (Leaf Curl)"},
                {"id": "spots", "name": "కాయ మచ్చ తెగులు/కుళ్ళు (Fruit Spots/Rot)"},
            ],
        },
        "mr": {
            "parts": [
                {"id": "leaves", "name": "पाने (Leaves)"},
                {"id": "fruit", "name": "मिरची फळ (Fruit)"},
            ],
            "observations": [
                {"id": "curl", "name": "पर्णगुच्छ/पाने आखडणे (Leaf Curl)"},
                {"id": "spots", "name": "फळावर डाग/सड (Fruit Spots/Rot)"},
            ],
        },
    },
    "paddy": {
        "hi": {
            "parts": [
                {"id": "leaves", "name": "पत्तियां (Leaves)"},
                {"id": "fruit", "name": "दाना/बाली (Grain)"},
            ],
            "observations": [
                {"id": "blast", "name": "ब्लास्ट/पत्ती झुलसना (Blast/Leaf Blight)"},
                {"id": "rot", "name": "तने/बाली की सड़न (Grain discoloration)"},
            ],
        },
        "en": {
            "parts": [
                {"id": "leaves", "name": "Leaves"},
                {"id": "fruit", "name": "Grain/Ear"},
            ],
            "observations": [
                {"id": "blast", "name": "Leaf Blast/Blight spots"},
                {"id": "rot", "name": "Grain discoloration/Rot"},
            ],
        },
        "ta": {
            "parts": [
                {"id": "leaves", "name": "இலைகள் (Leaves)"},
                {"id": "fruit", "name": "நெல் மணி (Grain)"},
            ],
            "observations": [
                {"id": "blast", "name": "குலை நோய் (Blast)"},
                {"id": "rot", "name": "நெல்மணி கருநிறமாதல் (Grain discoloration)"},
            ],
        },
        "te": {
            "parts": [
                {"id": "leaves", "name": "ఆకులు (Leaves)"},
                {"id": "fruit", "name": "వరి గింజ (Grain)"},
            ],
            "observations": [
                {"id": "blast", "name": "అగ్గి తెగులు (Blast)"},
                {"id": "rot", "name": "వరి గింజ రంగు మారడం/కుళ్ళు (Grain discoloration)"},
            ],
        },
        "mr": {
            "parts": [
                {"id": "leaves", "name": "पाने (Leaves)"},
                {"id": "fruit", "name": "भात दाणे/कणिस (Grain)"},
            ],
            "observations": [
                {"id": "blast", "name": "करपा रोग (Blast)"},
                {"id": "rot", "name": "तांदूळ दाणे सडणे (Grain discoloration)"},
            ],
        },
    },
}

REMEDIES = {
    "tomato": {
        "leaves": {
            "spots": {
                "hi": {
                    "disease_name": "अगेती झुलसा (Early Blight)",
                    "organic_management": "1. नीम के तेल (Neem oil) 5 मिली प्रति लीटर पानी में मिलाकर छिड़काव करें।\n2. संक्रमित पत्तियों को हटा दें।\n3. तांबे के कवकनाशी (Copper fungicide) का उपयोग करें।"
                },
                "en": {
                    "disease_name": "Early Blight",
                    "organic_management": "1. Spray Neem oil (5ml/L of water) at 7-10 days intervals.\n2. Prune lower infected leaves to prevent soil splash.\n3. Apply copper-based fungicide if severe."
                },
                "ta": {
                    "disease_name": "ஆரம்பகால இலைக்கருகல் நோய் (Early Blight)",
                    "organic_management": "1. வேப்பெண்ணெய் (Neem oil) 5 மிலி ஒரு லிட்டர் தண்ணீரில் கலந்து தெளிக்கவும்.\n2. பாதிக்கப்பட்ட இலைகளை கவாத்து செய்யவும்.\n3. தாமிரம் சார்ந்த பூசணக்கொல்லியைப் பயன்படுத்தவும்."
                },
                "te": {
                    "disease_name": "ఆల్టర్నేరియా ఆకు మచ్చ తెగులు (Early Blight)",
                    "organic_management": "1. లీటరు నీటికి 5 మి.లీ. వేపనూనె కలిపి పిచికారీ చేయండి.\n2. సోకిన కింది ఆకులను కత్తిరించి నాశనం చేయండి.\n3. తెగులు తీవ్రంగా ఉంటే రాగి ఆధారిత శిలీంద్రనాశకాన్ని వాడండి."
                },
                "mr": {
                    "disease_name": "लवकर येणारा करपा (Early Blight)",
                    "organic_management": "1. ५ मिली प्रति लीटर पाण्यात कडुनिंबाचे तेल मिसळून फवारणी करावी.\n2. रोगट पाने काढून टाकावीत.\n3. तांबेयुक्त बुरशीनाशकाची फवारणी करावी."
                }
            },
            "yellowing": {
                "hi": {
                    "disease_name": "नाइट्रोजन की कमी या मोजेक वायरस (Mosaic Virus)",
                    "organic_management": "1. कंपोस्ट चाय (Compost tea) या वर्मीकंपोस्ट डालें।\n2. मोजेक वायरस वाली पत्तियों को उखाड़कर नष्ट करें ताकि अन्य पौधों में न फैले।"
                },
                "en": {
                    "disease_name": "Nitrogen Deficiency / Mosaic Virus",
                    "organic_management": "1. Apply nitrogen-rich organic compost or vermicompost.\n2. If virus is suspected, pull out and destroy infected plants to stop the spread."
                },
                "ta": {
                    "disease_name": "நைட்ரஜன் குறைபாடு / மொசைக் வைரஸ்",
                    "organic_management": "1. நைட்ரஜன் நிறைந்த மட்கிய உரங்களை பயன்படுத்தவும்.\n2. மொசைக் வைரஸ் பாதிக்கப்பட்ட செடிகளை வேரோடு பிடுங்கி அழிக்கவும்."
                },
                "te": {
                    "disease_name": "నత్రజని లోపం / మొజాయిక్ వైరస్",
                    "organic_management": "1. నత్రజని పుష్కలంగా ఉన్న వర్మీకంపోస్ట్ లేదా సేంద్రీయ ఎరువును వాడండి.\n2. వైరస్ సోకిన మొక్కలను పీకి తగులబెట్టండి."
                },
                "mr": {
                    "disease_name": "नत्र कमतरता / मोझॅक व्हायरस",
                    "organic_management": "1. नत्रयुक्त सेंद्रिय खत किंवा गांडूळ खत वापरावे.\n2. विषाणू बाधित रोपे उपटून नष्ट करावीत."
                }
            }
        },
        "fruit": {
            "rot": {
                "hi": {
                    "disease_name": "ब्लॉसम एंड रॉट (Blossom End Rot)",
                    "organic_management": "1. मिट्टी में कैल्शियम (Calcium) की कमी पूरी करें।\n2. पानी की मात्रा नियंत्रित रखें, मिट्टी में ज्यादा सूखापन न आने दें।"
                },
                "en": {
                    "disease_name": "Blossom End Rot",
                    "organic_management": "1. Add calcium to the soil (lime or crushed eggshells).\n2. Water regularly and maintain even soil moisture; avoid dry spells."
                },
                "ta": {
                    "disease_name": "பூவடி அழுகல் நோய் (Blossom End Rot)",
                    "organic_management": "1. மண்ணில் கால்சியம் சத்தை அதிகரிக்கவும் (முட்டை ஓடு அல்லது சுண்ணாம்பு).\n2. சீரான நீர் மேலாண்மையை கடைபிடிக்கவும்."
                },
                "te": {
                    "disease_name": "కాయ కుళ్ళు తెగులు (Blossom End Rot)",
                    "organic_management": "1. నేలలో కాల్షియం లోపాన్ని నివారించండి (సున్నం లేదా గుడ్డు పెంకులు వాడండి).\n2. క్రమం తప్పకుండా నీరు పెట్టండి."
                },
                "mr": {
                    "disease_name": "फळांचा शेंडा कुजणे (Blossom End Rot)",
                    "organic_management": "1. जमिनीत कॅल्शियमचे प्रमाण वाढवावे.\n2. पाण्याचे नियोजन नियमित ठेवावे, जास्त कोरडेपणा येऊ देऊ नये."
                }
            }
        }
    },
    "wheat": {
        "leaves": {
            "yellowing": {
                "hi": {
                    "disease_name": "नाइट्रोजन की कमी (Nitrogen Deficiency)",
                    "organic_management": "1. यूरिया या जैविक खाद (Vermicompost) का प्रयोग करें।\n2. खेत में उचित जल निकासी सुनिश्चित करें।"
                },
                "en": {
                    "disease_name": "Nitrogen Deficiency",
                    "organic_management": "1. Top-dress with well-decomposed organic manure or vermicompost.\n2. Ensure proper irrigation and drainage in the field."
                },
                "ta": {
                    "disease_name": "நைட்ரஜன் குறைபாடு (Nitrogen Deficiency)",
                    "organic_management": "1. மட்கிய உரங்களை இடவும்.\n2. வயலில் நீர் தேங்காமல் வடிகால் வசதியை ஏற்படுத்தவும்."
                },
                "te": {
                    "disease_name": "నత్రజని లోపం (Nitrogen Deficiency)",
                    "organic_management": "1. బాగా కుళ్ళిన సేంద్రీయ ఎరువు లేదా వర్మీకంపోస్ట్ వేయండి.\n2. పొలంలో సరైన నీటి పారుదల ఉండేలా చూసుకోండి."
                },
                "mr": {
                    "disease_name": "नत्राची कमतरता (Nitrogen Deficiency)",
                    "organic_management": "1. युरिया किंवा गांडूळ खताचा वापर करावा.\n2. शेतात पाण्याचा निचरा चांगला ठेवावा."
                }
            },
            "rust": {
                "hi": {
                    "disease_name": "गेहूं का रस्ट रोग (Wheat Rust)",
                    "organic_management": "1. प्रतिरोधी किस्मों के बीज लगाएं।\n2. खट्टा छाछ (Sour buttermilk) का छिड़काव करें या उपयुक्त जैविक कवकनाशी का प्रयोग करें।"
                },
                "en": {
                    "disease_name": "Wheat Rust (Rust Disease)",
                    "organic_management": "1. Use rust-resistant seed varieties for planting.\n2. Spray sour buttermilk solution or organic copper fungicide."
                },
                "ta": {
                    "disease_name": "துரு நோய் (Wheat Rust)",
                    "organic_management": "1. நோய் எதிர்ப்பு ரக விதைகளைப் பயன்படுத்தவும்.\n2. புளித்த மோர் கரைசல் தெளிக்கவும்."
                },
                "te": {
                    "disease_name": "గోధుమ తుప్పు తెగులు (Wheat Rust)",
                    "organic_management": "1. తెగులు తట్టుకునే రకాలను ఎంచుకోండి.\n2. పుల్లటి మజ్జిగ ద్రావణాన్ని పిచिकారీ చేయండి."
                },
                "mr": {
                    "disease_name": "तांबेरा रोग (Wheat Rust)",
                    "organic_management": "1. रोगप्रतिकारक जातींचे बियाणे वापरावे.\n2. आंबट ताकाची फवारणी करावी."
                }
            }
        }
    },
    "potato": {
        "leaves": {
            "blight": {
                "hi": {
                    "disease_name": "पछैती झुलसा (Late Blight)",
                    "organic_management": "1. तांबे के कवकनाशी (Copper fungicide) का छिड़काव करें।\n2. अत्यधिक नमी से बचें, सुबह सिंचाई करें।"
                },
                "en": {
                    "disease_name": "Late Blight of Potato",
                    "organic_management": "1. Spray organic copper fungicide immediately when spots appear.\n2. Avoid overhead irrigation to minimize leaf wetness."
                },
                "ta": {
                    "disease_name": "பின்கால இலைக்கருகல் நோய் (Late Blight)",
                    "organic_management": "1. தாமிரம் பூசணக்கொல்லியைத் தெளிக்கவும்.\n2. இலைகளில் நீண்ட நேரம் நீர் தங்காதவாறு பார்த்துக் கொள்ளவும்."
                },
                "te": {
                    "disease_name": "లేట్ బ్లైట్ తెగులు (Late Blight)",
                    "organic_management": "1. రాగి శిలీంద్రనాశకాన్ని వెంటనే పిచికారీ చేయండి.\n2. ఆకులు నిరంతరం తడిగా ఉండకుండా చూసుకోండి."
                },
                "mr": {
                    "disease_name": "उशिरा येणारा करपा (Late Blight)",
                    "organic_management": "1. बोर्डो मिश्रण किंवा तांबेयुक्त बुरशीनाशक फवारावे.\n2. सकाळी पाणी द्यावे जेणेकरून दिवसभर पाने कोरडी राहतील."
                }
            }
        },
        "tuber": {
            "rot": {
                "hi": {
                    "disease_name": "सॉफ्ट रॉट (Soft Rot)",
                    "organic_management": "1. जल निकासी अच्छी रखें।\n2. ग्रसित आलू को हटा दें।\n3. फसल चक्र (Crop rotation) अपनाएं।"
                },
                "en": {
                    "disease_name": "Tuber Soft Rot",
                    "organic_management": "1. Ensure excellent soil drainage; avoid waterlogging.\n2. Harvest when soil is dry and discard rotten tubers.\n3. Practice crop rotation."
                },
                "ta": {
                    "disease_name": "மென்மையான அழுகல் நோய் (Soft Rot)",
                    "organic_management": "1. வயலில் நீர் தேங்குவதை தவிர்க்கவும்.\n2. அழுகிய கிழங்குகளை அகற்றவும். 3. பயிர் சுழற்சி முறை பின்பற்றவும்."
                },
                "te": {
                    "disease_name": "మెత్తటి కుళ్ళు తెగులు (Soft Rot)",
                    "organic_management": "1. నీటి పారుదల సరిగ్గా ఉండేలా చూసుకోండి.\n2. సోకిన దుంపలను తొలగించండి. 3. పంట మార్పిడి పద్ధతిని పాటించండి."
                },
                "mr": {
                    "disease_name": "मऊ कूज रोग (Soft Rot)",
                    "organic_management": "1. पाण्याचा निचरा चांगला ठेवावा.\n2. बाधित बटाटे काढून टाकावेत. ३. पीक पालट पद्धत वापरावी."
                }
            }
        }
    },
    "chilli": {
        "leaves": {
            "curl": {
                "hi": {
                    "disease_name": "लीफ कर्ल रोग (Leaf Curl Virus)",
                    "organic_management": "1. सफेद मक्खी (Whitefly) को नियंत्रित करने के लिए पीले चिपचिपे जाल (Yellow sticky traps) लगाएं।\n2. नीम के काढ़े (Neem decoction) का हर 10 दिन में छिड़काव करें।"
                },
                "en": {
                    "disease_name": "Leaf Curl Virus",
                    "organic_management": "1. Use yellow sticky traps to control the whitefly vector.\n2. Spray neem seed kernel extract or neem oil every 10 days."
                },
                "ta": {
                    "disease_name": "இலைச்சுருட்டல் நோய் (Leaf Curl)",
                    "organic_management": "1. வெள்ளை ஈக்களைக் கட்டுப்படுத்த மஞ்சள் ஒட்டும் பொறிகளைப் பயன்படுத்தவும்.\n2. 10 நாட்களுக்கு ஒருமுறை வேப்ப எண்ணெய் தெளிக்கவும்."
                },
                "te": {
                    "disease_name": "ఆకు ముడత తెగులు (Leaf Curl)",
                    "organic_management": "1. తెల్లదోమల నివారణకు పసుపు రంగు జిగురు కార్డ్‌లను వాడండి.\n2. 10 రోజుల వ్యవధిలో వేపనూనె పిచికారీ చేయండి."
                },
                "mr": {
                    "disease_name": "पाने आखडणे/चुरडा-मुरडा (Leaf Curl)",
                    "organic_management": "1. पांढरी माशी नियंत्रणासाठी पिवळे चिकट सापळे लावावेत.\n2. कडुनिंबाच्या अर्काची दर १० दिवसांनी फवारणी करावी."
                }
            }
        }
    },
    "paddy": {
        "leaves": {
            "blast": {
                "hi": {
                    "disease_name": "धान का ब्लास्ट रोग (Rice Blast)",
                    "organic_management": "1. संतुलित मात्रा में नाइट्रोजन डालें।\n2. ट्राइकोडर्मा (Trichoderma) जैव-कवकनाशी का छिड़काव करें।"
                },
                "en": {
                    "disease_name": "Rice Blast",
                    "organic_management": "1. Avoid excessive application of nitrogen fertilizers.\n2. Spray Trichoderma viride bio-fungicide formulation."
                },
                "ta": {
                    "disease_name": "நெல் குலை நோய் (Rice Blast)",
                    "organic_management": "1. தழைச்சத்து (Nitrogen) உரம் அதிகமாக இடுவதை தவிர்க்கவும்.\n2. ட்ரைகோடெர்மா (Trichoderma) பூஞ்சணக்கொல்லி தெளிக்கவும்."
                },
                "te": {
                    "disease_name": "వరి అగ్గి తెగులు (Rice Blast)",
                    "organic_management": "1. నత్రజని ఎరువుల వాడకాన్ని తగ్గించండి.\n2. ట్రైకోడెర్మా విరిడే వంటి జీవ శిలీంద్రనాశకాలను పిచికారీ చేయండి."
                },
                "mr": {
                    "disease_name": "भातावरील करपा (Rice Blast)",
                    "organic_management": "1. नत्राचा संतुलित वापर करावा.\n2. ट्रायकोडर्मा या जैविक बुरशीनाशकाची फवारणी करावी."
                }
            }
        }
    }
}


def get_crops(lang: str = "en") -> list[dict]:
    """Retrieve translated crops list for the specified language."""
    key = lang.lower()
    # Check exact match first
    if key in CROPS:
        return CROPS[key]
    # Check starting pattern (e.g. 'en-US' -> 'en')
    for code in CROPS.keys():
        if key.startswith(code):
            return CROPS[code]
    return CROPS["en"]


def get_symptoms(crop_id: str, lang: str = "en") -> dict:
    """Retrieve translated symptoms list for the crop."""
    key = lang.lower()
    crop_data = SYMPTOMS.get(crop_id.lower())
    if not crop_data:
        return {"parts": [], "observations": []}

    # Match language code
    matched_code = "en"
    if key in crop_data:
        matched_code = key
    else:
        for code in crop_data.keys():
            if key.startswith(code):
                matched_code = code
                break

    return crop_data[matched_code]


def get_remedy(crop_id: str, part: str, observation: str, lang: str = "en") -> dict:
    """Retrieve translated organic remedy for the crop infection."""
    key = lang.lower()

    # Determine matched language code
    matched_code = "en"
    if key.startswith("hi"):
        matched_code = "hi"
    elif key.startswith("ta"):
        matched_code = "ta"
    elif key.startswith("te"):
        matched_code = "te"
    elif key.startswith("mr"):
        matched_code = "mr"

    fallback_remedy = {
        "hi": {
            "disease_name": "सामान्य रोग (General Disease)",
            "organic_management": "प्रभावित भागों को नष्ट कर दें। नीम के तेल (Neem Oil) का छिड़काव करें।",
        },
        "en": {
            "disease_name": "General Infection",
            "organic_management": "Prune and destroy infected parts. Apply neem oil spray and maintain proper irrigation.",
        },
        "ta": {
            "disease_name": "பொதுவான நோய் (General Infection)",
            "organic_management": "பாதிக்கப்பட்ட பகுதிகளை அகற்றி அழிக்கவும். வேப்பெண்ணெய் தெளிக்கவும்.",
        },
        "te": {
            "disease_name": "సాధారణ తెగులు (General Disease)",
            "organic_management": "సోకిన భాగాలను తొలగించి నాశనం చేయండి. వేపనూనె పిచికారీ చేయండి.",
        },
        "mr": {
            "disease_name": "सामान्य रोग (General Disease)",
            "organic_management": "बाधित भाग कापून नष्ट करावेत. कडुनिंबाच्या तेलाची फवारणी करावी.",
        },
    }

    crop = REMEDIES.get(crop_id.lower())
    if not crop:
        return fallback_remedy[matched_code]

    plant_part = crop.get(part.lower())
    if not plant_part:
        return fallback_remedy[matched_code]

    obs = plant_part.get(observation.lower())
    if not obs:
        return fallback_remedy[matched_code]

    return obs.get(matched_code, obs["en"])
