# --- Build 'mkmk' Feature (Mark → Mark Stacking) ---

Font = Glyphs.font
selectedGlyphs = [l.parent for l in Font.selectedLayers]

# Configurable
featureName = "mkmk"
markClassTag = "@Marks"
baseAnchorName = "top"
markAnchorName = "_top"

# Helper
def findAnchor(layer, anchorName):
    for anchor in layer.anchors:
        if anchor.name == anchorName:
            return anchor
    return None

# Step 1: Select marks that have both anchors
markGlyphs = []

for glyph in selectedGlyphs:
    masterLayer = glyph.layers[Font.selectedFontMaster.id]
    if not masterLayer or not masterLayer.anchors:
        continue
    if findAnchor(masterLayer, baseAnchorName) and findAnchor(masterLayer, markAnchorName):
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

# Step 3: Build mark-to-mark lookups
markLookups = []
for mark in markGlyphs:
    masterLayer = mark.layers[Font.selectedFontMaster.id]
    anchor = findAnchor(masterLayer, baseAnchorName)
    if anchor:
        markLookups.append(
            "pos mark {} <{} {}> mark {};".format(
                mark.name, int(anchor.position.x), int(anchor.position.y), markClassTag
            )
        )

# Step 4: Assemble feature
featureCode = """
    {markClasses}
    lookup mark_mark {{
        {mark}
    }} mark_mark;
""".format(
    markClasses="\n    ".join(markClasses),
    mark="\n        ".join(markLookups)
)

# Step 5: Insert feature
for i, feature in enumerate(Font.features):
    if feature.name == featureName:
        del Font.features[i]
        break

newFeature = GSFeature(name=featureName, code=featureCode)
Font.features.append(newFeature)

# Report
print("✅ 'mkmk' feature built!")
print("✅ Marks:", len(markGlyphs))
