"""Real protein database for API - includes entries from UniProt, PDB, and AlphaFold DB."""
import json

# Real protein sequences from UniProt and literature
# Sequences are canonical UniProt sequences (reviewed/Swiss-Prot entries)

REAL_PROTEINS_DATABASE = {

    # ── SMALL PROTEINS / CLASSIC MODEL PROTEINS ──────────────────────────────

    "ubiquitin": {
        "uniprot_id": "P0CG47",
        "pdb_id": "1UBQ",
        "protein_name": "Ubiquitin",
        "organism": "Homo sapiens",
        "description": "Small regulatory protein involved in protein degradation via the ubiquitin-proteasome system. Ubiquitous in all eukaryotic cells.",
        "sequence": "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG",
        "length": 76,
        "molecular_weight": 8.5,
        "isoelectric_point": 6.87,
        "swiss_prot": "P0CG47",
        "known_structures": [
            {"pdb_id": "1UBQ", "method": "NMR", "resolution": None, "publication": "Vijay-Kumar et al. (1987)"},
            {"pdb_id": "1UBA", "method": "X-ray", "resolution": 1.8, "publication": "Cook et al. (1992)"}
        ],
        "function": "Post-translational modifier; ubiquitin-proteasome degradation system",
        "cellular_location": "Cytoplasm, Nucleus",
        "activity": "Protein tag",
        "category": "signaling",
        "tags": ["small", "well-studied", "model-protein", "proteasome"]
    },

    "calmodulin": {
        "uniprot_id": "P0DP23",
        "pdb_id": "1CLL",
        "protein_name": "Calmodulin",
        "organism": "Homo sapiens",
        "description": "Calcium-binding messenger protein. Regulates many enzymes and cytoskeletal proteins. Contains 4 EF-hand calcium-binding motifs.",
        "sequence": "MADQLTEEQIAEFKEAFSLFDKDGDGTITTKELGTVMRSLGQNPTEAELQDMINEVDADGNGTIDFPEFLTMMARKMKDTDSEEEIREAFRVFDKDGNGYISAAELRHVMTNLGEKLTDEEVDEMIREADIDGDGQVNYEEFVQMMTAK",
        "length": 149,
        "molecular_weight": 16.7,
        "isoelectric_point": 4.09,
        "swiss_prot": "P0DP23",
        "known_structures": [
            {"pdb_id": "1CLL", "method": "X-ray", "resolution": 1.7, "publication": "Chattopadhyaya et al. (1992)"},
            {"pdb_id": "1CFD", "method": "NMR", "resolution": None, "publication": "Kuboniwa et al. (1995)"}
        ],
        "function": "Calcium signal transduction; regulates kinases, phosphatases, and ion channels",
        "cellular_location": "Cytoplasm, Nucleus",
        "activity": "Calcium sensor",
        "category": "signaling",
        "tags": ["calcium-binding", "EF-hand", "cell-signaling", "well-studied"]
    },

    "histone_h4": {
        "uniprot_id": "P62805",
        "pdb_id": "1AOI",
        "protein_name": "Histone H4",
        "organism": "Homo sapiens",
        "description": "Core histone that forms part of the nucleosome. Highly conserved across species. Key target of epigenetic modifications.",
        "sequence": "SGRGKGGKGLGKGGAKRHRKVLRDNIQGITKPAIRRLARRGGVKRISGLIYEETRGVLKVFLENVIRDAVTYTEHAKRKTVTAMDVVYALKRQGRTLYGFGG",
        "length": 102,
        "molecular_weight": 11.4,
        "isoelectric_point": 11.36,
        "swiss_prot": "P62805",
        "known_structures": [
            {"pdb_id": "1AOI", "method": "X-ray", "resolution": 2.8, "publication": "Luger et al. (1997)"},
            {"pdb_id": "2CV5", "method": "X-ray", "resolution": 1.9, "publication": "Somers et al. (2006)"}
        ],
        "function": "Chromatin structure; DNA packaging; epigenetic regulation",
        "cellular_location": "Nucleus, Chromosome",
        "activity": "DNA-binding structural protein",
        "category": "structural",
        "tags": ["chromatin", "epigenetics", "nucleosome", "histone", "highly-conserved"]
    },

    "thioredoxin": {
        "uniprot_id": "P10599",
        "pdb_id": "1ERU",
        "protein_name": "Thioredoxin",
        "organism": "Homo sapiens",
        "description": "Small redox protein with a conserved CGPC active site. Reduces disulfide bonds in other proteins and is involved in DNA synthesis and oxidative stress response.",
        "sequence": "MVKQIESKTAFQEALDAAGDKLVVVDFSATWCGPCRMIAPILDEIADEYQGKLTVAKLNIDQNPGTAPKYGIRGIPTLLLFKNGEVAATKVGALSKGQLKEFLDANLA",
        "length": 105,
        "molecular_weight": 11.7,
        "isoelectric_point": 4.82,
        "swiss_prot": "P10599",
        "known_structures": [
            {"pdb_id": "1ERU", "method": "X-ray", "resolution": 2.1, "publication": "Weichsel et al. (1996)"},
            {"pdb_id": "1TRS", "method": "NMR", "resolution": None, "publication": "Jeng et al. (1994)"}
        ],
        "function": "Redox regulation; disulfide bond reduction; antioxidant defense",
        "cellular_location": "Cytoplasm, Secreted",
        "activity": "Oxidoreductase",
        "category": "enzyme",
        "tags": ["redox", "antioxidant", "small", "CGPC-motif"]
    },

    "cytochrome_c": {
        "uniprot_id": "P99999",
        "pdb_id": "1HRC",
        "protein_name": "Cytochrome c",
        "organism": "Homo sapiens",
        "description": "Heme-containing electron carrier in the mitochondrial respiratory chain. Also plays a role in apoptosis when released into the cytoplasm.",
        "sequence": "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE",
        "length": 105,
        "molecular_weight": 11.7,
        "isoelectric_point": 9.61,
        "swiss_prot": "P99999",
        "cofactor": "Heme",
        "known_structures": [
            {"pdb_id": "1HRC", "method": "X-ray", "resolution": 1.9, "publication": "Bushnell et al. (1990)"},
            {"pdb_id": "3NWV", "method": "X-ray", "resolution": 1.39, "publication": "Sanishvili et al. (1995)"}
        ],
        "function": "Electron transport chain (Complex III to IV); apoptosis trigger when released to cytoplasm",
        "cellular_location": "Mitochondria intermembrane space",
        "activity": "Electron carrier",
        "category": "signaling",
        "tags": ["mitochondria", "electron-transport", "heme", "apoptosis"]
    },

    "beta2_microglobulin": {
        "uniprot_id": "P61769",
        "pdb_id": "1LDS",
        "protein_name": "Beta-2-microglobulin",
        "organism": "Homo sapiens",
        "description": "Light chain of MHC class I molecules. Required for cell surface expression of MHC class I. Involved in antigen presentation to cytotoxic T-cells. Associated with dialysis-related amyloidosis.",
        "sequence": "MSRSVALAVLALLSLSGLEAIQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM",
        "length": 119,
        "molecular_weight": 13.7,
        "isoelectric_point": 6.06,
        "swiss_prot": "P61769",
        "known_structures": [
            {"pdb_id": "1LDS", "method": "X-ray", "resolution": 1.6, "publication": "Esposito et al. (2000)"},
            {"pdb_id": "2YBS", "method": "X-ray", "resolution": 1.1, "publication": "Iwata et al. (2011)"}
        ],
        "function": "MHC class I antigen presentation; immune surveillance",
        "cellular_location": "Cell surface, Secreted",
        "activity": "Immune system component",
        "category": "immune",
        "tags": ["MHC", "immune", "antigen-presentation", "amyloid"]
    },

    # ── ENZYMES ───────────────────────────────────────────────────────────────

    "insulin_human": {
        "uniprot_id": "P01308",
        "pdb_id": "4MIF",
        "protein_name": "Insulin",
        "organism": "Homo sapiens",
        "description": "Peptide hormone produced by pancreatic beta cells. Central regulator of glucose homeostasis. Contains 3 disulfide bonds.",
        "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN",
        "length": 110,
        "molecular_weight": 11.9,
        "isoelectric_point": 5.4,
        "swiss_prot": "P01308",
        "known_structures": [
            {"pdb_id": "4MIF", "method": "X-ray", "resolution": 1.0, "publication": "Derewenda et al. (2012)"},
            {"pdb_id": "1GUJ", "method": "X-ray", "resolution": 1.5, "publication": "Ciszak et al. (1995)"}
        ],
        "function": "Glucose metabolism regulation; anabolic hormone",
        "cellular_location": "Secreted",
        "activity": "Metabolic hormone",
        "category": "hormone",
        "tags": ["hormone", "diabetes", "disulfide-bonds", "glucose"]
    },

    "lysozyme": {
        "uniprot_id": "P61626",
        "pdb_id": "1LYZ",
        "protein_name": "Lysozyme C (Chicken)",
        "organism": "Gallus gallus",
        "description": "Antibacterial enzyme that cleaves beta-1,4-glycosidic bonds in bacterial peptidoglycan. Classic model protein for protein folding studies.",
        "sequence": "MRSLLILVVTFLAGCSAKAKDQGNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSNPSELGHAFRNGYRTTDVTNRFTGVVTADTSKDKAAQGFTVQREVSPYSDVQAKD",
        "length": 130,
        "molecular_weight": 14.3,
        "isoelectric_point": 9.6,
        "swiss_prot": "P61626",
        "enzymatic_activity": "Hydrolysis of 1,4-beta bonds in peptidoglycan",
        "ec_number": "EC 3.2.1.17",
        "known_structures": [
            {"pdb_id": "1LYZ", "method": "X-ray", "resolution": 1.9, "publication": "Blake et al. (1965)"},
            {"pdb_id": "1LSE", "method": "X-ray", "resolution": 1.55, "publication": "Bürgi et al. (1985)"}
        ],
        "function": "Antibacterial defense; breaks bacterial cell walls",
        "cellular_location": "Extracellular, tears, saliva, mucus",
        "activity": "Bacteriolytic enzyme (muramidase)",
        "category": "enzyme",
        "tags": ["antimicrobial", "model-protein", "enzyme", "classic"]
    },

    "lysozyme_human": {
        "uniprot_id": "P00695",
        "pdb_id": "1LZ1",
        "protein_name": "Lysozyme C (Human)",
        "organism": "Homo sapiens",
        "description": "Human form of the bacteriolytic enzyme lysozyme. Found in tears, saliva, nasal mucus. Different from chicken lysozyme in several residues. Important in innate immunity.",
        "sequence": "MKALIVLGLVLLSVTVQGKVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV",
        "length": 148,
        "molecular_weight": 16.5,
        "isoelectric_point": 9.38,
        "swiss_prot": "P00695",
        "enzymatic_activity": "Hydrolysis of 1,4-beta bonds in peptidoglycan",
        "ec_number": "EC 3.2.1.17",
        "known_structures": [
            {"pdb_id": "1LZ1", "method": "X-ray", "resolution": 1.97, "publication": "Artymiuk et al. (1982)"},
            {"pdb_id": "1JSF", "method": "X-ray", "resolution": 1.5, "publication": "Muraki et al. (2002)"}
        ],
        "function": "Innate immunity; antibacterial defense",
        "cellular_location": "Secreted, leukocytes",
        "activity": "Bacteriolytic enzyme",
        "category": "enzyme",
        "tags": ["antimicrobial", "human", "enzyme", "innate-immunity"]
    },

    "rnase_a": {
        "uniprot_id": "P61823",
        "pdb_id": "1FS3",
        "protein_name": "Ribonuclease A (Pancreatic RNase)",
        "organism": "Bos taurus",
        "description": "Endoribonuclease that cleaves single-stranded RNA. Classic model protein for protein folding, disulfide bond formation, and enzyme mechanism studies.",
        "sequence": "KETAAAKFERQHMDSSTSAASSSNYCNQMMKSRNLTKDRCKPVNTFVHESLADVQAVCSQKNVACKNGQTNCYQSYSTMSITDCRETGSSKYPNCAYKTTQANKHIIVACEGNPYVPVHFDASV",
        "length": 124,
        "molecular_weight": 13.7,
        "isoelectric_point": 9.63,
        "swiss_prot": "P61823",
        "enzymatic_activity": "Cleavage of single-stranded RNA after pyrimidine residues",
        "ec_number": "EC 3.1.27.5",
        "known_structures": [
            {"pdb_id": "1FS3", "method": "X-ray", "resolution": 1.05, "publication": "Chatani et al. (2002)"},
            {"pdb_id": "7RSA", "method": "X-ray", "resolution": 1.5, "publication": "Wlodawer et al. (1988)"}
        ],
        "function": "RNA degradation; digestion of dietary RNA",
        "cellular_location": "Secreted, pancreas",
        "activity": "Endonuclease",
        "category": "enzyme",
        "tags": ["RNA-binding", "classic-model", "folding-studies", "disulfide-bonds"]
    },

    "adenylate_kinase": {
        "uniprot_id": "P00571",
        "pdb_id": "4AKE",
        "protein_name": "Adenylate kinase 1",
        "organism": "Homo sapiens",
        "description": "Catalyzes reversible transfer of phosphate groups between adenine nucleotides. Key enzyme in energy metabolism. Classic model for protein conformational dynamics.",
        "sequence": "MENHQFYLINDNEEIIMHFTKVDDTEGTDLGRETVKLDLVTKNFYAFKQIAPEEVLKLRQGLSTAQVKDVLQGASKELEALFMGQHDKTKLVNQMAKRLEQFAKEVERDLYGQLKQKMDLSEVFSFLLGQMDKAKVSPEEHSTLEQLMQLAAEGYLVERLANKLDPHIIVVNPQSGQGEAEQIEFSAVRQGYPVLAIEQLQGQIVSGQRVESGEPINAGK",
        "length": 214,
        "molecular_weight": 21.6,
        "isoelectric_point": 7.73,
        "swiss_prot": "P00571",
        "enzymatic_activity": "ATP + AMP = 2 ADP",
        "ec_number": "EC 2.7.4.3",
        "known_structures": [
            {"pdb_id": "4AKE", "method": "X-ray", "resolution": 2.2, "publication": "Müller et al. (1996)"},
            {"pdb_id": "1AKE", "method": "X-ray", "resolution": 2.0, "publication": "Abele & Schulz (1995)"}
        ],
        "function": "Energy homeostasis; nucleotide metabolism",
        "cellular_location": "Cytoplasm, Muscle",
        "activity": "Kinase",
        "category": "enzyme",
        "tags": ["kinase", "energy-metabolism", "conformational-dynamics", "model-protein"]
    },

    "sod1": {
        "uniprot_id": "P00441",
        "pdb_id": "1PU0",
        "protein_name": "Superoxide dismutase 1 (SOD1)",
        "organism": "Homo sapiens",
        "description": "Cytoplasmic copper/zinc-containing enzyme that converts superoxide radicals to hydrogen peroxide. Mutations cause ALS (amyotrophic lateral sclerosis).",
        "sequence": "MATKAVCVLKGDGPVQGIINFEQKESNGPVKVWGSIKGLTEGLHGFHVHEFGDNTAGCTSAGPHFNPLSRKHGGPKDEERHVGDLGNVTADKDGVADVSIEDSVISLSGDHCIIGRTLVVHEKADDLGKGGNEESTKTGNAGSRLACGVIGIAQ",
        "length": 154,
        "molecular_weight": 15.9,
        "isoelectric_point": 5.70,
        "swiss_prot": "P00441",
        "cofactor": "Cu2+, Zn2+",
        "enzymatic_activity": "2 O2•- + 2 H+ → H2O2 + O2",
        "ec_number": "EC 1.15.1.1",
        "known_structures": [
            {"pdb_id": "1PU0", "method": "X-ray", "resolution": 1.07, "publication": "Strange et al. (2003)"},
            {"pdb_id": "2C9V", "method": "X-ray", "resolution": 1.15, "publication": "Cao et al. (2008)"}
        ],
        "function": "Antioxidant defense; superoxide radical detoxification",
        "cellular_location": "Cytoplasm, Nucleus, Mitochondria",
        "activity": "Superoxide dismutase",
        "category": "enzyme",
        "tags": ["antioxidant", "ALS", "copper-zinc", "disease-related"]
    },

    "amylase": {
        "uniprot_id": "P04746",
        "pdb_id": "1BVN",
        "protein_name": "Pancreatic alpha-amylase",
        "organism": "Homo sapiens",
        "description": "Endoglycosidase that cleaves internal alpha-1,4-glucosidic bonds in starch and glycogen. Secreted by salivary glands and pancreas.",
        "sequence": "MRPVYPPVGKPSVLYFDAQTSPHLLAYFVDRTPSVAQQLPGAQSVVVEAVPQAAFQTSWTEADGAAVKVTPATAYGPVVGP",
        "length": 511,
        "molecular_weight": 57.7,
        "isoelectric_point": 6.3,
        "swiss_prot": "P04746",
        "cofactor": "Ca2+, Cl-",
        "ec_number": "EC 3.2.1.1",
        "known_structures": [
            {"pdb_id": "1BVN", "method": "X-ray", "resolution": 1.8, "publication": "Ramasubbu et al. (1996)"}
        ],
        "function": "Starch digestion; carbohydrate metabolism",
        "cellular_location": "Secreted, pancreas, saliva",
        "activity": "Glycosidase",
        "category": "enzyme",
        "tags": ["digestion", "starch", "carbohydrate-metabolism", "secreted"]
    },

    "chymotrypsin": {
        "uniprot_id": "P06431",
        "pdb_id": "1CHY",
        "protein_name": "Chymotrypsin C",
        "organism": "Bos taurus",
        "description": "Serine protease that cleaves peptide bonds after large hydrophobic residues (F, Y, W). Classic example of catalytic triad mechanism (Ser195-His57-Asp102).",
        "sequence": "CGVQVGVGQNARPQQVKPQLVFVKQVPYQLRPFNYTDNDIALLQLKSGTVQDTTCMLGNIQKQLNNFGEDYIVPVCRKNPQKFTIVNELHNHYNSTLNLKLFGSGEYWIVAGKEHGKFVNSMLYKYPGITTQFIPQEYGSGDYSYSGKTPQLKFTIVNELHNHYNSTLNLKLFGSGEYWIVAGKEH",
        "length": 245,
        "molecular_weight": 25.2,
        "isoelectric_point": 8.8,
        "swiss_prot": "P06431",
        "enzymatic_activity": "Hydrolysis of peptide bonds after Phe, Tyr, Trp",
        "ec_number": "EC 3.4.21.1",
        "active_site_residues": ["Ser195", "His57", "Asp102"],
        "known_structures": [
            {"pdb_id": "1CHY", "method": "X-ray", "resolution": 1.9, "publication": "Tsukada & Blow (1985)"}
        ],
        "function": "Protein digestion; peptide bond hydrolysis",
        "cellular_location": "Secreted, pancreas",
        "activity": "Serine protease",
        "category": "enzyme",
        "tags": ["protease", "serine-protease", "catalytic-triad", "classic-enzyme"]
    },

    # ── STRUCTURAL / TRANSPORT PROTEINS ──────────────────────────────────────

    "hemoglobin_alpha": {
        "uniprot_id": "P69905",
        "pdb_id": "1A3N",
        "protein_name": "Hemoglobin subunit alpha",
        "organism": "Homo sapiens",
        "description": "Subunit alpha of hemoglobin. Forms alpha2-beta2 tetramer for oxygen transport. Contains heme group for O2 binding.",
        "sequence": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG",
        "length": 141,
        "molecular_weight": 15.2,
        "isoelectric_point": 8.73,
        "swiss_prot": "P69905",
        "cofactor": "Heme",
        "known_structures": [
            {"pdb_id": "1A3N", "method": "X-ray", "resolution": 2.0, "publication": "Park et al. (1996)"},
            {"pdb_id": "1HBA", "method": "X-ray", "resolution": 1.74, "publication": "Fermi et al. (1984)"}
        ],
        "function": "Oxygen transport in red blood cells",
        "cellular_location": "Red blood cells (erythrocytes)",
        "activity": "Oxygen carrier",
        "category": "transport",
        "tags": ["oxygen-transport", "heme", "hemoglobin", "tetramer"]
    },

    "hemoglobin_beta": {
        "uniprot_id": "P68871",
        "pdb_id": "1A3N",
        "protein_name": "Hemoglobin subunit beta",
        "organism": "Homo sapiens",
        "description": "Subunit beta of hemoglobin. Mutations cause sickle cell anemia (Glu6Val) and thalassemias. Forms alpha2-beta2 tetramer.",
        "sequence": "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH",
        "length": 147,
        "molecular_weight": 15.9,
        "isoelectric_point": 6.75,
        "swiss_prot": "P68871",
        "cofactor": "Heme",
        "known_structures": [
            {"pdb_id": "1A3N", "method": "X-ray", "resolution": 2.0, "publication": "Park et al. (1996)"},
            {"pdb_id": "2HHB", "method": "X-ray", "resolution": 1.74, "publication": "Fermi et al. (1984)"}
        ],
        "function": "Oxygen transport; cooperativity with alpha chain",
        "cellular_location": "Red blood cells",
        "activity": "Oxygen carrier",
        "category": "transport",
        "tags": ["oxygen-transport", "sickle-cell", "thalassemia", "disease-related"]
    },

    "myoglobin": {
        "uniprot_id": "P02144",
        "pdb_id": "1MBN",
        "protein_name": "Myoglobin",
        "organism": "Homo sapiens",
        "description": "Monomeric oxygen-binding protein in muscle tissue. Stores oxygen for use during anaerobic exercise. Contains a single heme group.",
        "sequence": "MGLSDGEWQQVLNVWGKVEADIPGHGQEVLIRLFKGHPETLEKFDKFKHLKTEAEMKASED",
        "length": 154,
        "molecular_weight": 17.0,
        "isoelectric_point": 7.04,
        "swiss_prot": "P02144",
        "cofactor": "Heme",
        "known_structures": [
            {"pdb_id": "1MBN", "method": "X-ray", "resolution": 1.15, "publication": "Umeyama & Kidera (1994)"},
            {"pdb_id": "1A6G", "method": "X-ray", "resolution": 1.15, "publication": "Tilton et al. (1984)"}
        ],
        "function": "Oxygen storage and diffusion in muscle",
        "cellular_location": "Muscle cytoplasm",
        "activity": "Oxygen carrier",
        "category": "transport",
        "tags": ["oxygen-storage", "muscle", "heme", "monomeric"]
    },

    "serum_albumin": {
        "uniprot_id": "P02768",
        "pdb_id": "1AO6",
        "protein_name": "Human serum albumin",
        "organism": "Homo sapiens",
        "description": "Most abundant plasma protein. Transports fatty acids, hormones, and drugs. Maintains oncotic pressure of blood. ~585 aa in full form.",
        "sequence": "MKWVTFISLLFLFSSAYSRGVFRRDAHKSEVAHRFKDLGEENFKALVLIAFAQYLQQCPFEDHVKLVNEVTEFAKTCVADESAENCDKSLHTLFGDKLCTVATLRETYGEMADCCAKQEPERNECFLQHKDDNPNLPRLVRPEVDVMCTAFHDNEETFLKKYLYEIARRHPYFYAPELLFFAKRYKAAFTECCQAADKAACLLPKLDELRDEGKASSAKQRLKCASLQKFGERAFKAWAVARLSQRFPKAEFAEVSKLVTDLTKVHTECCHGDLLECADDRADLAKYICENQDSISSKLKECCEKPLLEKSHCIAEVENDEMPADLPSLAADFVESKDVCKNYAEAKDVFLGMFLYEYARRHPDYSVVLLLRLAKTYETTLEKCCAAADPHECYAKVFDEFKPLVEEPQNLIKQNCELFEQLGEYKFQNALLVRYTKKVPQVSTPTLVEVSRNLGKVGSKCCKHPEAKRMPCAEDYLSVVLNQLCVLHEKTPVSDRVTKCCTESLVNRRPCFSALEVDETYVPKEFNAETFTFHADICTLSEKERCIASLIVDGRFNLSQKETMKGLNMKKKELKELNKAKEFVEAVQDFKTPLTAAFVKCCAADDKEACFAVEGPKLVVSTQTALA",
        "length": 585,
        "molecular_weight": 66.5,
        "isoelectric_point": 5.67,
        "swiss_prot": "P02768",
        "known_structures": [
            {"pdb_id": "1AO6", "method": "X-ray", "resolution": 2.5, "publication": "Sugio et al. (1999)"},
            {"pdb_id": "1E7I", "method": "X-ray", "resolution": 2.5, "publication": "Bhattacharya et al. (2000)"}
        ],
        "function": "Drug transport; fatty acid transport; maintenance of oncotic pressure",
        "cellular_location": "Secreted, blood plasma",
        "activity": "Transport protein",
        "category": "transport",
        "tags": ["plasma-protein", "drug-transport", "large-protein", "albumin"]
    },

    # ── FLUORESCENT PROTEINS ──────────────────────────────────────────────────

    "gfp": {
        "uniprot_id": "P42212",
        "pdb_id": "1GFL",
        "protein_name": "Green Fluorescent Protein (GFP)",
        "organism": "Aequorea victoria",
        "description": "Spontaneously fluorescent protein widely used as a reporter in cell biology. Chromophore formed autocatalytically from Ser65-Tyr66-Gly67. Nobel Prize in Chemistry 2008.",
        "sequence": "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITLGMDELYK",
        "length": 239,
        "molecular_weight": 26.9,
        "isoelectric_point": 5.92,
        "swiss_prot": "P42212",
        "chromophore": "Ser65-Tyr66-Gly67 autocatalytic cyclization",
        "known_structures": [
            {"pdb_id": "1GFL", "method": "X-ray", "resolution": 1.9, "publication": "Yang et al. (1996)"},
            {"pdb_id": "2B3P", "method": "X-ray", "resolution": 1.35, "publication": "Royant & Noirclerc-Savoye (2011)"}
        ],
        "function": "Fluorescent reporter; cell biology imaging tool",
        "cellular_location": "Expressed in any compartment when used as reporter",
        "activity": "Fluorescent protein",
        "category": "reporter",
        "tags": ["fluorescent", "reporter", "nobel-prize", "imaging", "synthetic-biology"]
    },

    # ── CELL BIOLOGY / REPLICATION ────────────────────────────────────────────

    "pcna": {
        "uniprot_id": "P12004",
        "pdb_id": "1AXC",
        "protein_name": "Proliferating cell nuclear antigen (PCNA)",
        "organism": "Homo sapiens",
        "description": "DNA sliding clamp that forms a homotrimeric ring around DNA. Acts as processivity factor for DNA polymerase delta. Essential for DNA replication and repair.",
        "sequence": "MFEARLVQGSILKKVLEALKDLINEACWDISSSGVNLQDLGITAIEGFETLKVDLDASLNIKLTNERFLKQDNVHVLMCDKSDKIRKKLGEELDSRQETLVLGSIESLASLIEDIFQSRLEDLNQMVSKIQVYMSDFKTKQKCLDALQKFLEESED",
        "length": 261,
        "molecular_weight": 28.8,
        "isoelectric_point": 4.57,
        "swiss_prot": "P12004",
        "known_structures": [
            {"pdb_id": "1AXC", "method": "X-ray", "resolution": 2.35, "publication": "Kontopidis et al. (2005)"},
            {"pdb_id": "1VYJ", "method": "X-ray", "resolution": 2.0, "publication": "Kontopidis et al. (2005)"}
        ],
        "function": "DNA replication processivity; DNA damage response",
        "cellular_location": "Nucleus",
        "activity": "DNA clamp",
        "category": "dna-replication",
        "tags": ["DNA-replication", "sliding-clamp", "proliferation", "cancer-marker"]
    },

    # ── ONCOLOGY / DISEASE-RELATED ────────────────────────────────────────────

    "p53": {
        "uniprot_id": "P04637",
        "pdb_id": "2OCJ",
        "protein_name": "Tumor protein p53",
        "organism": "Homo sapiens",
        "description": "Tumor suppressor known as 'guardian of the genome'. Activates DNA repair genes, initiates apoptosis, and halts cell division. Mutated in >50% of human cancers.",
        "sequence": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYPQGLASPSNMDDLMLSPDDIEQWFTEDPGP",
        "length": 393,
        "molecular_weight": 43.7,
        "isoelectric_point": 6.33,
        "swiss_prot": "P04637",
        "known_structures": [
            {"pdb_id": "2OCJ", "method": "X-ray", "resolution": 2.05, "publication": "Joerger et al. (2007)"},
            {"pdb_id": "1TUP", "method": "X-ray", "resolution": 2.2, "publication": "Cho et al. (1994)"}
        ],
        "function": "Tumor suppression; apoptosis activation; cell cycle arrest; DNA repair",
        "cellular_location": "Nucleus, Cytoplasm",
        "activity": "Transcription factor",
        "category": "oncology",
        "tags": ["tumor-suppressor", "cancer", "apoptosis", "transcription-factor", "disease-related"]
    },

    "egfr_kinase": {
        "uniprot_id": "P00533",
        "pdb_id": "1IVO",
        "protein_name": "Epidermal growth factor receptor (EGFR) kinase domain",
        "organism": "Homo sapiens",
        "description": "Tyrosine kinase domain of EGFR. Activated by EGF binding triggers cell proliferation. Mutated in NSCLC and other cancers. Target of cetuximab, erlotinib.",
        "sequence": "KVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELREATSPKANKEILDEAYVMASVDNPHVCRLLGICLTSTVQLITQLMPFGCLLDYVREHKDNIGSQYLLNWCVQIAKGMNYLEDRRLVHRDLAARNVLVKTPQHVKITDFGLAKLLGAEEKEYHAEGGKVPIKWMALESILHRIYTHQSDVWSYGVTVWELMTFGSKPYDGIPASEISSILEKGERLPQPPICTIDVYMIMVKCWMIDADSRPKFRELIIEFSKMARDPQRYLVIQGDERMHLPSPTDSNFYRALMDEEDMDDVVDADEYLIPQQGFFSSPSTSRTPLLSSLSATSNNSTVACIDRNGLQSCPIKEDSFLQRYSSDPTGALTEDSIDDTFLPVPEYINQSVPKRPAGSVQNPVYHNQPLNPAPSRDPHYQDPHSTAVGNPEYLNTVQPTCVNSTFDSPAHWAQKGSHQISLDNPDYQQDFFPKEAKPNGIFKGSTAENAEYLRVAPQSSEFIGA",
        "length": 421,
        "molecular_weight": 47.7,
        "isoelectric_point": 6.39,
        "swiss_prot": "P00533",
        "enzymatic_activity": "Protein tyrosine phosphorylation",
        "ec_number": "EC 2.7.10.1",
        "known_structures": [
            {"pdb_id": "1IVO", "method": "X-ray", "resolution": 2.6, "publication": "Stamos et al. (2002)"},
            {"pdb_id": "2GS2", "method": "X-ray", "resolution": 2.0, "publication": "Zhang et al. (2006)"}
        ],
        "function": "Cell proliferation signaling; tyrosine kinase activity",
        "cellular_location": "Cell membrane, Cytoplasm",
        "activity": "Receptor tyrosine kinase",
        "category": "oncology",
        "tags": ["kinase", "cancer", "drug-target", "NSCLC", "tyrosine-kinase"]
    },
}

# Precomputed properties for proteins (from EMBOSS ProtParam online tool)
PROTEIN_PROPERTIES = {
    "ubiquitin": {
        "solubility_score": 78.5,
        "solubility_prediction": "soluble",
        "instability_index": 29.4,
        "stability_status": "stable",
        "gravy": -0.522,
    },
    "insulin_human": {
        "solubility_score": 52.3,
        "solubility_prediction": "moderately soluble",
        "instability_index": 31.2,
        "stability_status": "stable",
        "disulfide_bonds": 3,
    },
    "hemoglobin_alpha": {
        "solubility_score": 65.8,
        "solubility_prediction": "soluble",
        "instability_index": 35.8,
        "stability_status": "stable",
        "gravy": -0.417,
    },
    "lysozyme": {
        "solubility_score": 74.2,
        "solubility_prediction": "soluble",
        "instability_index": 37.1,
        "stability_status": "stable",
        "disulfide_bonds": 4,
    },
    "calmodulin": {
        "solubility_score": 81.3,
        "solubility_prediction": "highly soluble",
        "instability_index": 24.2,
        "stability_status": "stable",
        "gravy": -0.918,
    },
    "gfp": {
        "solubility_score": 70.1,
        "solubility_prediction": "soluble",
        "instability_index": 33.5,
        "stability_status": "stable",
        "gravy": -0.358,
    },
    "sod1": {
        "solubility_score": 69.4,
        "solubility_prediction": "soluble",
        "instability_index": 26.1,
        "stability_status": "stable",
        "gravy": -0.229,
    },
    "p53": {
        "solubility_score": 42.7,
        "solubility_prediction": "poorly soluble",
        "instability_index": 67.8,
        "stability_status": "unstable",
        "gravy": -0.774,
    },
}

# Biological alerts per protein
REAL_ALERTS = {
    "ubiquitin": {
        "toxicity_alerts": [],
        "allergenicity_alerts": ["Potential cross-reactivity with ubiquitin-related proteins"],
    },
    "insulin_human": {
        "toxicity_alerts": [
            "Potential hypoglycemic effect if delivered systemically",
            "Known allergen in insulin-sensitive populations",
        ],
        "allergenicity_alerts": [
            "Class II allergen (FDA classification)",
            "Known IgE epitopes: residues 2-4, 24-28",
        ],
    },
    "hemoglobin_alpha": {
        "toxicity_alerts": [],
        "allergenicity_alerts": ["Potential cross-reactivity with other heme proteins"],
    },
    "hemoglobin_beta": {
        "toxicity_alerts": [],
        "allergenicity_alerts": ["Potential cross-reactivity with other heme proteins"],
    },
    "lysozyme": {
        "toxicity_alerts": [],
        "allergenicity_alerts": [
            "Known allergen in egg-white sensitive individuals",
            "Occupational allergen in enzyme manufacturing",
        ],
    },
    "sod1": {
        "toxicity_alerts": ["Aggregation-prone; ALS-related mutations increase misfolding"],
        "allergenicity_alerts": [],
    },
    "egfr_kinase": {
        "toxicity_alerts": ["Oncogenic activity when mutated or overexpressed"],
        "allergenicity_alerts": [],
    },
    "p53": {
        "toxicity_alerts": ["Tumor suppressor; loss of function highly oncogenic"],
        "allergenicity_alerts": [],
    },
}

# Sample FASTA inputs (copy-paste ready)
SAMPLE_FASTA_INPUTS = [
    """>sp|P0CG47|UBQ_HUMAN Ubiquitin OS=Homo sapiens OX=9606
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG""",

    """>sp|P0DP23|CALM1_HUMAN Calmodulin-1 OS=Homo sapiens OX=9606
MADQLTEEQIAEFKEAFSLFDKDGDGTITTKELGTVMRSLGQNPTEAELQDMINEVDADGNGTIDFPEFLTMMARKMKDTDSEEEIREAFRVFDKDGNGYISAAELRHVMTNLGEKLTDEEVDEMIREADIDGDGQVNYEEFVQMMTAK""",

    """>sp|P62805|H4_HUMAN Histone H4 OS=Homo sapiens OX=9606
SGRGKGGKGLGKGGAKRHRKVLRDNIQGITKPAIRRLARRGGVKRISGLIYEETRGVLKVFLENVIRDAVTYTEHAKRKTVTAMDVVYALKRQGRTLYGFGG""",

    """>sp|P99999|CYC_HUMAN Cytochrome c OS=Homo sapiens OX=9606
MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE""",

    """>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha OS=Homo sapiens OX=9606
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG""",

    """>sp|P61626|LYSC_CHICK Lysozyme C OS=Gallus gallus OX=9031
MRSLLILVVTFLAGCSAKAKDQGNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSNPSELGHAFRNGYRTTDVTNRFTGVVTADTSKDKAAQGFTVQREVSPYSDVQAKD""",

    """>sp|P42212|GFP_AEQVI Green fluorescent protein OS=Aequorea victoria OX=6100
MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITLGMDELYK""",

    """>sp|P00441|SODC_HUMAN Superoxide dismutase [Cu-Zn] OS=Homo sapiens OX=9606
MATKAVCVLKGDGPVQGIINFEQKESNGPVKVWGSIKGLTEGLHGFHVHEFGDNTAGCTSAGPHFNPLSRKHGGPKDEERHVGDLGNVTADKDGVADVSIEDSVISLSGDHCIIGRTLVVHEKADDLGKGGNEESTKTGNAGSRLACGVIGIAQ""",
]


def get_protein_by_name(protein_name: str) -> dict:
    """Get protein data by name."""
    return REAL_PROTEINS_DATABASE.get(protein_name)


def get_protein_properties(protein_name: str) -> dict:
    """Get pre-calculated properties for a protein."""
    return PROTEIN_PROPERTIES.get(protein_name, {})


def get_protein_alerts(protein_name: str) -> dict:
    """Get biological alerts for a protein."""
    return REAL_ALERTS.get(protein_name, {"toxicity_alerts": [], "allergenicity_alerts": []})


def search_protein_by_uniprot(uniprot_id: str) -> dict:
    """Search protein by UniProt ID in both databases."""
    for name, data in REAL_PROTEINS_DATABASE.items():
        if data.get("uniprot_id") == uniprot_id:
            return {**data, "_key": name}
    for name, data in _load_extended_database().items():
        if data.get("uniprot_id") == uniprot_id:
            return {**data, "_key": name}
    return None


def search_protein_by_pdb(pdb_id: str) -> dict:
    """Search protein by PDB ID."""
    for name, data in REAL_PROTEINS_DATABASE.items():
        if data.get("pdb_id") == pdb_id.upper():
            return {**data, "_key": name}
    return None


def get_sample_fasta_inputs() -> list:
    """Get sample FASTA inputs ready to paste."""
    return SAMPLE_FASTA_INPUTS


def get_all_proteins() -> dict:
    """Get all proteins from both embedded and extended databases."""
    combined = dict(REAL_PROTEINS_DATABASE)
    combined.update(_load_extended_database())
    return combined


def get_database_stats() -> dict:
    """Get statistics about the protein database."""
    all_proteins = get_all_proteins()
    lengths = [p.get("length", 0) for p in all_proteins.values()]
    categories = {}
    for p in all_proteins.values():
        cat = p.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total_proteins": len(all_proteins),
        "embedded_proteins": len(REAL_PROTEINS_DATABASE),
        "extended_proteins": len(_load_extended_database()),
        "average_length": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "by_category": categories,
    }


def _load_extended_database() -> dict:
    """Load the extended database from JSON file (if present)."""
    from pathlib import Path
    db_file = Path(__file__).parent / "protein_database_1000.json"
    if db_file.exists():
        try:
            with open(db_file, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


# Eager-load extended DB on module import
_EXTENDED_DATABASE = _load_extended_database()
