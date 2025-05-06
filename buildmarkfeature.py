# --- Build 'mark' Feature (Base → Mark) ---

Font = Glyphs.font
selectedGlyphs = [l.parent for l in Font.selectedLayers]

# Configurable
featureName = "mark"
markClassTag = "@Marks"
baseAnchorName = "top"
markAnchorName = "_top"

# Helper
def findAnchor(layer, anchorName):
    for anchor in layer.anchors:
        if anchor.name == anchorName:
            return anchor
    return None

# Step 1: Separate bases and marks
baseGlyphs = []
markGlyphs = []

for glyph in selectedGlyphs:
    masterLayer = glyph.layers[Font.selectedFontMaster.id]
    if not masterLayer or not masterLayer.anchors:
        continue
    if findAnchor(masterLayer, baseAnchorName):
        baseGlyphs.append(glyph)
    elif findAnchor(masterLayer, markAnchorName):
        markGlyphs.append(glyph)

# Step 2: Build markClasses
markClasses = []
for mark in markGlyphs:
    masterLayer = mark.layers[Font.selectedFontMaster.id]
    anchor = findAnchor(masterLayer, markAnchorName)
    if anchor:
        markClasses.append(
            "markClass {} <{} {}> {};".format(
                mark.name, int(anchor.position.x), int(anchor.position.y), markClassTag
            )
        )

# Step 3: Build base lookups
baseLookups = []
for base in baseGlyphs:
    masterLayer = base.layers[Font.selectedFontMaster.id]
    anchor = findAnchor(masterLayer, baseAnchorName)
    if anchor:
        baseLookups.append(
            "pos base {} <{} {}> mark {};".format(
                base.name, int(anchor.position.x), int(anchor.position.y), markClassTag
            )
        )

# Step 4: Assemble feature
featureCode = """
    {markClasses}
    lookup mark_base {{
        {base}
    }} mark_base;
""".format(
    markClasses="\n    ".join(markClasses),
    base="\n        ".join(baseLookups)
)

# Step 5: Insert feature
for i, feature in enumerate(Font.features):
    if feature.name == featureName:
        del Font.features[i]
        break

newFeature = GSFeature(name=featureName, code=featureCode)
Font.features.append(newFeature)

# Report
print("✅ 'mark' feature built!")
print("✅ Bases:", len(baseGlyphs))
print("✅ Marks:", len(markGlyphs))
