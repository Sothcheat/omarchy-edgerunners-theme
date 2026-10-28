#!/usr/bin/env python3
"""Build the Edgerunners themes for VS Code and Zed from ../colors.toml.

    python3 editors/build.py

Writes editors/vscode/ (a flat extension: package.json, the theme JSON and the
two files a .vsix needs) and editors/zed/edgerunners.json.

Syntax follows One Monokai's structure, where every role gets its own hue so
no two kinds of token read alike, with Edgerunners colours in each slot:

    keywords, operators, tags       neon red     (One Monokai pink-red)
    declaration words, constants,
      built-in types, JSON keys     Lucy cyan        (cyan)
    functions, attributes           acid green       (green)
    classes, types, modules         Lucy blue      (blue)
    strings                         rocket gold     (yellow)
    numbers, template ${}           neon violet   (purple)
    parameters                      HOTEL orange, italic
    this / self                     neon red, italic
    properties, object keys         neon pink (One Dark gives them a hue too)
    comments                        rain haze, italic
    variables                       lavender (plain text)

The UI keeps neon red for errors only; focus, selection and the active tab
use the Lucy cyan, as the Omarchy shell does.
"""
import json
import pathlib
import tomllib

HERE = pathlib.Path(__file__).resolve().parent
P = tomllib.loads((HERE.parent / "colors.toml").read_text())

BG = P["background"]
FG = P["foreground"]
C = {
    "keyword": P["red"],
    "storage": P["cyan"],
    "function": P["green"],
    "type": P["blue"],
    "string": P["yellow"],  # rocket gold: 8.2:1 on bg
    "number": P["magenta"],
    "param": P["orange"],
    "comment": P["muted"],
    "punct": P["dark_foreground"],
    "var": FG,
    # Neon pink, between keyword red and number violet (OKLCH 0.78 0.16 350):
    # 9.0:1 on bg, 14.8 ΔE from keywords, 15.8 from numbers. ANSI bright red
    # was too pale to tell from plain text.
    "property": "#FE8CC5",
}
UI = {
    "bg": BG,
    "panel": P["dark_background"],
    "deep": P["darker_background"],
    "raised": "#151635",
    "line": "#151632",
    "border": "#1E2040",
    "hover": "#01293E",
    "select": P["selection"],
    "accent": P["cyan"],
    "accent_dim": "#028397",
    "button": "#046E7F",
    "guide": "#222447",
    "guide_active": "#4A4E78",
    "muted": P["muted"],
    "fg": FG,
    "fg_dim": P["dark_foreground"],
    "fg_bright": P["bright_foreground"],
}


def a(color, alpha):
    """#RRGGBB plus a two-digit hex alpha."""
    return f"{color}{alpha}"


# --------------------------------------------------------------------- VS Code
def vscode_colors():
    u, p = UI, P
    return {
        "focusBorder": u["accent_dim"],
        "foreground": u["fg"],
        "disabledForeground": u["muted"],
        "descriptionForeground": u["fg_dim"],
        "errorForeground": p["red"],
        "icon.foreground": u["fg_dim"],
        "widget.border": u["border"],
        "widget.shadow": a(u["deep"], "99"),
        "selection.background": a(u["select"], "cc"),
        "sash.hoverBorder": u["accent_dim"],
        "textLink.foreground": p["cyan"],
        "textLink.activeForeground": p["bright_cyan"],
        "textBlockQuote.background": u["panel"],
        "textBlockQuote.border": u["accent_dim"],
        "textCodeBlock.background": u["panel"],
        "textPreformat.foreground": p["cyan"],
        "textSeparator.foreground": u["border"],

        "editor.background": u["bg"],
        "editor.foreground": u["fg"],
        "editorCursor.foreground": u["fg_bright"],
        "editorLineNumber.foreground": "#41446E",
        "editorLineNumber.activeForeground": u["fg_dim"],
        "editor.lineHighlightBackground": u["line"],
        "editor.lineHighlightBorder": "#00000000",
        "editor.selectionBackground": a(u["select"], "cc"),
        "editor.inactiveSelectionBackground": a(u["select"], "66"),
        "editor.selectionHighlightBackground": a(p["cyan"], "26"),
        "editor.wordHighlightBackground": a(p["cyan"], "22"),
        "editor.wordHighlightStrongBackground": a(p["cyan"], "38"),
        "editor.findMatchBackground": a(C["string"], "55"),
        "editor.findMatchBorder": C["string"],
        "editor.findMatchHighlightBackground": a(C["string"], "26"),
        "editor.findRangeHighlightBackground": a(u["select"], "44"),
        "editor.hoverHighlightBackground": a(p["cyan"], "1a"),
        "editor.rangeHighlightBackground": a(u["select"], "44"),
        "editor.foldBackground": a(u["select"], "33"),
        "editorWhitespace.foreground": "#2A2D51",
        "editorRuler.foreground": u["border"],
        "editorCodeLens.foreground": u["muted"],
        "editorLink.activeForeground": p["cyan"],
        "editorIndentGuide.background1": u["guide"],
        "editorIndentGuide.activeBackground1": u["guide_active"],
        "editorBracketMatch.background": a(p["cyan"], "22"),
        "editorBracketMatch.border": a(p["cyan"], "99"),
        "editorBracketHighlight.foreground1": C["string"],
        "editorBracketHighlight.foreground2": p["magenta"],
        "editorBracketHighlight.foreground3": p["cyan"],
        "editorBracketHighlight.foreground4": p["orange"],
        "editorBracketHighlight.foreground5": p["green"],
        "editorBracketHighlight.foreground6": p["blue"],
        "editorBracketHighlight.unexpectedBracket.foreground": p["red"],
        "editorBracketPairGuide.activeBackground1": a(C["string"], "88"),
        "editorBracketPairGuide.activeBackground2": a(p["magenta"], "88"),
        "editorBracketPairGuide.activeBackground3": a(p["cyan"], "88"),
        "editorError.foreground": p["red"],
        "editorWarning.foreground": C["string"],
        "editorInfo.foreground": p["blue"],
        "editorHint.foreground": p["cyan"],
        "editorUnnecessaryCode.opacity": "#000000aa",
        "editorGutter.background": u["bg"],
        "editorGutter.addedBackground": p["green"],
        "editorGutter.modifiedBackground": C["string"],
        "editorGutter.deletedBackground": p["red"],
        "editorGutter.foldingControlForeground": u["fg_dim"],
        "editorOverviewRuler.border": "#00000000",
        "editorOverviewRuler.addedForeground": a(p["green"], "99"),
        "editorOverviewRuler.modifiedForeground": a(C["string"], "99"),
        "editorOverviewRuler.deletedForeground": a(p["red"], "99"),
        "editorOverviewRuler.errorForeground": p["red"],
        "editorOverviewRuler.warningForeground": C["string"],
        "editorOverviewRuler.findMatchForeground": a(C["string"], "aa"),
        "editorInlayHint.background": a(u["select"], "66"),
        "editorInlayHint.foreground": u["muted"],
        "editorInlayHint.typeForeground": a(p["blue"], "bb"),
        "editorInlayHint.parameterForeground": a(p["orange"], "bb"),
        "editorGhostText.foreground": "#585C88",
        "editorStickyScroll.background": u["bg"],
        "editorStickyScroll.border": u["border"],
        "editorStickyScroll.shadow": a(u["deep"], "99"),
        "editorStickyScrollHover.background": u["hover"],
        "minimap.background": u["bg"],
        "minimap.findMatchHighlight": a(C["string"], "aa"),
        "minimap.selectionHighlight": a(p["cyan"], "66"),
        "minimap.errorHighlight": p["red"],
        "minimap.warningHighlight": C["string"],
        "minimapSlider.background": a(u["select"], "55"),
        "minimapSlider.hoverBackground": a(u["select"], "88"),
        "minimapSlider.activeBackground": a(u["select"], "aa"),
        "minimapGutter.addedBackground": p["green"],
        "minimapGutter.modifiedBackground": C["string"],
        "minimapGutter.deletedBackground": p["red"],

        "editorWidget.background": u["raised"],
        "editorWidget.foreground": u["fg"],
        "editorWidget.border": u["border"],
        "editorWidget.resizeBorder": u["accent_dim"],
        "editorSuggestWidget.background": u["raised"],
        "editorSuggestWidget.border": u["border"],
        "editorSuggestWidget.foreground": u["fg"],
        "editorSuggestWidget.selectedBackground": u["select"],
        "editorSuggestWidget.selectedForeground": u["fg_bright"],
        "editorSuggestWidget.highlightForeground": p["cyan"],
        "editorSuggestWidget.focusHighlightForeground": p["bright_cyan"],
        "editorHoverWidget.background": u["raised"],
        "editorHoverWidget.border": u["border"],
        "editorHoverWidget.foreground": u["fg"],
        "editorHoverWidget.highlightForeground": p["cyan"],
        "editorHoverWidget.statusBarBackground": u["panel"],
        "debugToolBar.background": u["raised"],

        "activityBar.background": u["panel"],
        "activityBar.foreground": u["fg"],
        "activityBar.inactiveForeground": u["muted"],
        "activityBar.border": u["panel"],
        "activityBar.activeBorder": p["cyan"],
        "activityBar.activeBackground": a(u["select"], "55"),
        "activityBarBadge.background": p["cyan"],
        "activityBarBadge.foreground": u["deep"],
        "activityBarTop.foreground": u["fg"],
        "activityBarTop.inactiveForeground": u["muted"],
        "activityBarTop.activeBorder": p["cyan"],

        "sideBar.background": u["panel"],
        "sideBar.foreground": u["fg_dim"],
        "sideBar.border": u["panel"],
        "sideBarTitle.foreground": u["fg"],
        "sideBarSectionHeader.background": u["panel"],
        "sideBarSectionHeader.foreground": u["fg"],
        "sideBarSectionHeader.border": u["border"],
        "sideBarStickyScroll.background": u["panel"],
        "sideBarStickyScroll.border": u["border"],

        "list.activeSelectionBackground": u["select"],
        "list.activeSelectionForeground": u["fg_bright"],
        "list.activeSelectionIconForeground": u["fg_bright"],
        "list.inactiveSelectionBackground": a(u["select"], "99"),
        "list.inactiveSelectionForeground": u["fg"],
        "list.hoverBackground": u["hover"],
        "list.hoverForeground": u["fg"],
        "list.focusBackground": u["select"],
        "list.focusForeground": u["fg_bright"],
        "list.focusOutline": u["accent_dim"],
        "list.focusAndSelectionOutline": u["accent_dim"],
        "list.inactiveFocusOutline": u["border"],
        "list.highlightForeground": p["cyan"],
        "list.focusHighlightForeground": p["bright_cyan"],
        "list.filterMatchBackground": a(C["string"], "33"),
        "list.errorForeground": p["red"],
        "list.warningForeground": C["string"],
        "list.dropBackground": a(u["select"], "88"),
        "tree.indentGuidesStroke": u["guide"],
        "tree.inactiveIndentGuidesStroke": a(u["guide"], "88"),

        "tab.activeBackground": u["bg"],
        "tab.activeForeground": u["fg_bright"],
        "tab.activeBorder": u["bg"],
        "tab.activeBorderTop": p["cyan"],
        "tab.activeModifiedBorder": C["string"],
        "tab.inactiveBackground": u["panel"],
        "tab.inactiveForeground": u["muted"],
        "tab.inactiveModifiedBorder": a(C["string"], "66"),
        "tab.hoverBackground": u["hover"],
        "tab.hoverForeground": u["fg"],
        "tab.border": u["panel"],
        "tab.lastPinnedBorder": u["border"],
        "tab.unfocusedActiveBackground": u["bg"],
        "tab.unfocusedActiveForeground": u["fg_dim"],
        "tab.unfocusedActiveBorderTop": u["accent_dim"],
        "tab.unfocusedInactiveBackground": u["panel"],
        "tab.unfocusedInactiveForeground": u["muted"],
        "tab.unfocusedHoverBackground": u["hover"],
        "editorGroup.border": u["border"],
        "editorGroup.emptyBackground": u["bg"],
        "editorGroup.dropBackground": a(u["select"], "66"),
        "editorGroupHeader.tabsBackground": u["panel"],
        "editorGroupHeader.tabsBorder": u["panel"],
        "editorGroupHeader.noTabsBackground": u["bg"],
        "editorPane.background": u["bg"],
        "breadcrumb.foreground": u["muted"],
        "breadcrumb.focusForeground": u["fg"],
        "breadcrumb.activeSelectionForeground": p["cyan"],
        "breadcrumbPicker.background": u["raised"],

        "statusBar.background": u["panel"],
        "statusBar.foreground": u["fg_dim"],
        "statusBar.border": u["panel"],
        "statusBar.focusBorder": u["accent_dim"],
        "statusBar.debuggingBackground": p["orange"],
        "statusBar.debuggingForeground": u["deep"],
        "statusBar.noFolderBackground": u["panel"],
        "statusBarItem.hoverBackground": u["hover"],
        "statusBarItem.activeBackground": u["select"],
        "statusBarItem.remoteBackground": u["button"],
        "statusBarItem.remoteForeground": u["fg_bright"],
        "statusBarItem.errorForeground": p["red"],
        "statusBarItem.warningForeground": C["string"],
        "statusBarItem.prominentBackground": u["select"],

        "titleBar.activeBackground": u["panel"],
        "titleBar.activeForeground": u["fg"],
        "titleBar.inactiveBackground": u["panel"],
        "titleBar.inactiveForeground": u["muted"],
        "titleBar.border": u["panel"],
        "commandCenter.background": u["raised"],
        "commandCenter.foreground": u["fg_dim"],
        "commandCenter.border": u["border"],
        "commandCenter.activeBackground": u["hover"],
        "commandCenter.activeBorder": u["accent_dim"],
        "commandCenter.inactiveForeground": u["muted"],
        "commandCenter.inactiveBorder": u["border"],

        "panel.background": u["panel"],
        "panel.border": u["border"],
        "panelTitle.activeBorder": p["cyan"],
        "panelTitle.activeForeground": u["fg"],
        "panelTitle.inactiveForeground": u["muted"],
        "panelSectionHeader.background": u["panel"],
        "panelSectionHeader.foreground": u["fg"],
        "outputView.background": u["panel"],

        "terminal.background": u["panel"],
        "terminal.foreground": u["fg"],
        "terminal.selectionBackground": a(u["select"], "cc"),
        "terminal.inactiveSelectionBackground": a(u["select"], "66"),
        "terminal.findMatchBackground": a(C["string"], "55"),
        "terminalCursor.foreground": u["fg_bright"],
        "terminalCommandDecoration.defaultBackground": u["muted"],
        "terminalCommandDecoration.successBackground": p["green"],
        "terminalCommandDecoration.errorBackground": p["red"],
        "terminal.ansiBlack": p["lighter_background"],
        "terminal.ansiRed": p["red"],
        "terminal.ansiGreen": p["green"],
        "terminal.ansiYellow": p["yellow"],
        "terminal.ansiBlue": p["blue"],
        "terminal.ansiMagenta": p["magenta"],
        "terminal.ansiCyan": p["cyan"],
        "terminal.ansiWhite": p["light_foreground"],
        "terminal.ansiBrightBlack": u["muted"],
        "terminal.ansiBrightRed": p["bright_red"],
        "terminal.ansiBrightGreen": p["bright_green"],
        "terminal.ansiBrightYellow": p["bright_yellow"],
        "terminal.ansiBrightBlue": p["bright_blue"],
        "terminal.ansiBrightMagenta": p["bright_magenta"],
        "terminal.ansiBrightCyan": p["bright_cyan"],
        "terminal.ansiBrightWhite": p["bright_foreground"],

        "input.background": u["deep"],
        "input.border": u["border"],
        "input.foreground": u["fg"],
        "input.placeholderForeground": u["muted"],
        "inputOption.activeBorder": u["accent_dim"],
        "inputOption.activeBackground": a(u["select"], "99"),
        "inputOption.activeForeground": u["fg_bright"],
        "inputValidation.errorBackground": u["raised"],
        "inputValidation.errorBorder": p["red"],
        "inputValidation.warningBackground": u["raised"],
        "inputValidation.warningBorder": C["string"],
        "inputValidation.infoBackground": u["raised"],
        "inputValidation.infoBorder": p["blue"],
        "dropdown.background": u["raised"],
        "dropdown.border": u["border"],
        "dropdown.foreground": u["fg"],
        "dropdown.listBackground": u["raised"],
        "button.background": u["button"],
        "button.foreground": u["fg_bright"],
        "button.hoverBackground": u["accent_dim"],
        "button.border": "#00000000",
        "button.separator": a(u["fg_bright"], "44"),
        "button.secondaryBackground": u["hover"],
        "button.secondaryForeground": u["fg"],
        "button.secondaryHoverBackground": u["select"],
        "checkbox.background": u["deep"],
        "checkbox.border": u["border"],
        "checkbox.foreground": p["cyan"],
        "badge.background": u["select"],
        "badge.foreground": u["fg_bright"],
        "progressBar.background": p["cyan"],
        "scrollbar.shadow": a(u["deep"], "88"),
        "scrollbarSlider.background": a(u["select"], "66"),
        "scrollbarSlider.hoverBackground": a(u["select"], "aa"),
        "scrollbarSlider.activeBackground": u["select"],

        "gitDecoration.addedResourceForeground": p["green"],
        "gitDecoration.modifiedResourceForeground": C["string"],
        "gitDecoration.deletedResourceForeground": p["red"],
        "gitDecoration.renamedResourceForeground": p["cyan"],
        "gitDecoration.untrackedResourceForeground": p["bright_green"],
        "gitDecoration.ignoredResourceForeground": "#585C88",
        "gitDecoration.conflictingResourceForeground": p["magenta"],
        "gitDecoration.stageModifiedResourceForeground": p["yellow"],
        "gitDecoration.stageDeletedResourceForeground": p["red"],
        "gitDecoration.submoduleResourceForeground": p["blue"],

        "diffEditor.insertedTextBackground": a(p["green"], "26"),
        "diffEditor.removedTextBackground": a(p["red"], "26"),
        "diffEditor.insertedLineBackground": a(p["green"], "14"),
        "diffEditor.removedLineBackground": a(p["red"], "14"),
        "diffEditor.border": u["border"],
        "diffEditor.diagonalFill": a(u["border"], "88"),
        "diffEditorGutter.insertedLineBackground": a(p["green"], "26"),
        "diffEditorGutter.removedLineBackground": a(p["red"], "26"),
        "diffEditorOverview.insertedForeground": a(p["green"], "99"),
        "diffEditorOverview.removedForeground": a(p["red"], "99"),
        "merge.currentHeaderBackground": a(p["green"], "55"),
        "merge.currentContentBackground": a(p["green"], "1a"),
        "merge.incomingHeaderBackground": a(p["blue"], "55"),
        "merge.incomingContentBackground": a(p["blue"], "1a"),

        "peekView.border": u["accent_dim"],
        "peekViewEditor.background": u["panel"],
        "peekViewEditor.matchHighlightBackground": a(C["string"], "44"),
        "peekViewResult.background": u["raised"],
        "peekViewResult.selectionBackground": u["select"],
        "peekViewResult.fileForeground": u["fg"],
        "peekViewResult.lineForeground": u["fg_dim"],
        "peekViewResult.matchHighlightBackground": a(C["string"], "44"),
        "peekViewTitle.background": u["raised"],
        "peekViewTitleLabel.foreground": u["fg"],
        "peekViewTitleDescription.foreground": u["muted"],

        "notifications.background": u["raised"],
        "notifications.foreground": u["fg"],
        "notifications.border": u["border"],
        "notificationCenter.border": u["border"],
        "notificationCenterHeader.background": u["panel"],
        "notificationCenterHeader.foreground": u["fg"],
        "notificationLink.foreground": p["cyan"],
        "notificationToast.border": u["border"],
        "notificationsErrorIcon.foreground": p["red"],
        "notificationsWarningIcon.foreground": C["string"],
        "notificationsInfoIcon.foreground": p["blue"],
        "quickInput.background": u["raised"],
        "quickInput.foreground": u["fg"],
        "quickInputList.focusBackground": u["select"],
        "quickInputList.focusForeground": u["fg_bright"],
        "quickInputList.focusIconForeground": u["fg_bright"],
        "quickInputTitle.background": u["panel"],
        "pickerGroup.border": u["border"],
        "pickerGroup.foreground": p["cyan"],
        "keybindingLabel.background": u["hover"],
        "keybindingLabel.foreground": u["fg"],
        "keybindingLabel.border": u["border"],
        "keybindingLabel.bottomBorder": u["border"],
        "menu.background": u["raised"],
        "menu.foreground": u["fg"],
        "menu.selectionBackground": u["select"],
        "menu.selectionForeground": u["fg_bright"],
        "menu.separatorBackground": u["border"],
        "menu.border": u["border"],
        "menubar.selectionBackground": u["hover"],
        "settings.headerForeground": u["fg"],
        "settings.modifiedItemIndicator": C["string"],
        "settings.focusedRowBackground": a(u["select"], "44"),
        "welcomePage.tileBackground": u["raised"],
        "welcomePage.tileHoverBackground": u["hover"],
        "walkThrough.embeddedEditorBackground": u["panel"],
        "chat.requestBubbleBackground": u["raised"],
    }


def scope(scopes, fg=None, style=None):
    s = {}
    if fg:
        s["foreground"] = fg
    if style is not None:
        s["fontStyle"] = style
    return {"scope": scopes, "settings": s}


def vscode_token_colors():
    c = C
    return [
        scope(["comment", "punctuation.definition.comment", "string.comment"], c["comment"], "italic"),
        scope(["comment.block.documentation", "comment.block.javadoc"], c["comment"], "italic"),
        scope(["storage.type.class.jsdoc", "entity.name.type.instance.jsdoc"], c["type"], "italic"),
        scope(["variable.other.jsdoc", "comment.block.documentation variable"], c["param"], "italic"),

        # Keywords, operators, tags: neon red.
        scope(["keyword", "keyword.control", "keyword.operator.new", "keyword.operator.expression",
               "keyword.operator.logical", "keyword.operator.constructor", "storage", "storage.modifier",
               "keyword.other.important"], c["keyword"]),
        scope(["keyword.operator", "keyword.operator.assignment", "keyword.operator.arithmetic",
               "keyword.operator.comparison", "keyword.operator.relational", "keyword.operator.ternary",
               "keyword.operator.spread", "keyword.operator.rest", "storage.type.function.arrow"], c["keyword"]),
        scope(["entity.name.tag", "meta.tag.sgml", "punctuation.definition.tag.html"], c["keyword"]),
        scope(["variable.language", "variable.language.this", "variable.language.self",
               "variable.language.super", "variable.parameter.function.language.special"], c["keyword"], "italic"),

        # Declaration words, constants, built-in types, JSON keys: Lucy cyan.
        scope(["storage.type", "storage.type.function", "storage.type.class", "storage.type.interface",
               "storage.type.enum", "storage.type.type", "storage.type.namespace", "keyword.declaration",
               "keyword.function", "keyword.type"], c["storage"]),
        scope(["constant.language", "constant.character", "constant.other", "support.constant",
               "variable.other.enummember", "constant.other.symbol"], c["storage"]),
        scope(["support.type.primitive", "support.type.builtin", "support.type", "entity.name.type.primitive",
               "keyword.type.primitive"], c["storage"]),
        scope(["support.type.property-name.json", "support.dictionary.json",
               "meta.structure.dictionary.key.python"], c["storage"]),
        scope(["string.regexp", "constant.other.character-class.regexp", "keyword.operator.quantifier.regexp"],
              c["storage"]),

        # Functions and attributes: acid green.
        scope(["entity.name.function", "support.function", "meta.function-call entity.name.function",
               "entity.name.function.member", "variable.function", "entity.name.function-call",
               "support.function.builtin", "meta.function-call.generic"], c["function"]),
        scope(["entity.other.attribute-name", "meta.decorator", "entity.name.function.decorator",
               "punctuation.decorator", "storage.type.annotation", "entity.other.inherited-class"], c["function"]),

        # Classes, types, modules: Lucy blue.
        scope(["entity.name.type", "entity.name.class", "entity.name.type.class", "entity.name.type.interface",
               "entity.name.type.enum", "entity.name.type.alias", "entity.name.namespace", "entity.name.module",
               "support.class", "entity.name.type.module", "entity.other.inherited-class.python",
               "storage.modifier.import", "storage.modifier.package", "entity.name.scope-resolution"], c["type"]),
        scope(["entity.name.type.parameter", "meta.type.parameters entity.name.type"], c["type"], "italic"),

        # Strings: rocket gold.
        scope(["string", "string.template", "string.quoted", "punctuation.definition.string",
               "markup.inline.raw.string"], c["string"]),

        # Numbers and template interpolation: neon violet.
        scope(["constant.numeric", "keyword.other.unit", "constant.numeric.decimal"], c["number"]),
        scope(["punctuation.definition.template-expression", "punctuation.section.embedded",
               "string.embedded.begin", "string.embedded.end", "constant.character.escape",
               "constant.character.format.placeholder"], c["number"]),

        # Parameters: HOTEL orange, italic.
        scope(["variable.parameter", "meta.parameter variable", "entity.name.variable.parameter",
               "variable.parameter.function"], c["param"], "italic"),

        # Variables: plain lavender. Properties and object keys: neon pink.
        # Punctuation dimmer.
        scope(["variable", "variable.other", "variable.other.readwrite", "entity.name.variable"], c["var"]),
        scope(["variable.other.property", "variable.other.object.property", "meta.object-literal.key",
               "support.variable.property", "variable.other.constant.property"], c["property"]),
        scope(["punctuation", "meta.brace", "punctuation.separator", "punctuation.terminator",
               "punctuation.accessor", "meta.delimiter"], c["punct"]),

        # CSS
        scope(["support.type.property-name.css", "support.type.vendored.property-name"], c["property"]),
        scope(["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css",
               "entity.other.attribute-name.pseudo-class", "entity.other.attribute-name.pseudo-element"],
              c["function"]),
        scope(["support.constant.property-value.css", "support.constant.color"], c["storage"]),
        scope(["keyword.other.unit.css", "keyword.other.unit.scss"], c["number"]),

        # Markdown
        scope(["markup.heading", "entity.name.section.markdown", "markup.heading.setext"], c["keyword"], "bold"),
        scope(["punctuation.definition.heading.markdown"], c["comment"]),
        scope(["markup.bold"], c["string"], "bold"),
        scope(["markup.italic"], c["number"], "italic"),
        scope(["markup.strikethrough"], c["comment"], "strikethrough"),
        scope(["markup.underline.link", "string.other.link", "markup.underline.link.image"], c["type"]),
        scope(["markup.inline.raw", "markup.raw.block", "markup.fenced_code"], c["storage"]),
        scope(["markup.quote"], c["function"], "italic"),
        scope(["punctuation.definition.list.begin.markdown", "markup.list.numbered.bullet",
               "beginning.punctuation.definition.list.markdown"], c["string"]),

        # Diffs and errors
        scope(["markup.inserted", "meta.diff.header.to-file"], P["green"]),
        scope(["markup.deleted", "meta.diff.header.from-file"], P["red"]),
        scope(["markup.changed"], c["string"]),
        scope(["meta.diff.range", "meta.diff.header"], c["type"]),
        scope(["invalid", "invalid.illegal"], P["bright_foreground"]),
        scope(["invalid.deprecated"], c["string"], "strikethrough"),
    ]


def vscode_semantic():
    c = C
    return {
        "namespace": c["type"],
        "class": c["type"],
        "class.defaultLibrary": c["type"],
        "interface": c["type"],
        "enum": c["type"],
        "struct": c["type"],
        "type": c["type"],
        "type.defaultLibrary": c["storage"],
        "typeParameter": {"foreground": c["type"], "italic": True},
        "function": c["function"],
        "function.defaultLibrary": c["function"],
        "method": c["function"],
        "macro": c["function"],
        "decorator": c["function"],
        "parameter": {"foreground": c["param"], "italic": True},
        "variable": c["var"],
        "variable.readonly.defaultLibrary": c["storage"],
        "property": c["property"],
        "enumMember": c["storage"],
        "event": c["property"],
        "label": c["string"],
        "selfKeyword": {"foreground": c["keyword"], "italic": True},
        "*.deprecated": {"strikethrough": True},
    }


def build_vscode(out):
    out.mkdir(parents=True, exist_ok=True)
    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": "Edgerunners",
        "type": "dark",
        "semanticHighlighting": True,
        "colors": vscode_colors(),
        "tokenColors": vscode_token_colors(),
        "semanticTokenColors": vscode_semantic(),
    }
    (out / "edgerunners-color-theme.json").write_text(json.dumps(theme, indent=2) + "\n")
    version = "1.0.2"
    pkg = {
        "name": "edgerunners-theme",
        "displayName": "Edgerunners",
        "description": "Edgerunners dark theme: Night City neon after rain, with One Monokai-style syntax",
        "version": version,
        "publisher": "ohmylucifer",
        "engines": {"vscode": "^1.80.0"},
        "categories": ["Themes"],
        "contributes": {
            "themes": [{"label": "Edgerunners", "uiTheme": "vs-dark", "path": "./edgerunners-color-theme.json"}]
        },
    }
    (out / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (out / "extension.vsixmanifest").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id="edgerunners-theme" Version="{version}" Publisher="ohmylucifer" />
    <DisplayName>Edgerunners</DisplayName>
    <Description xml:space="preserve">{pkg["description"]}</Description>
    <Tags>theme,color-theme,dark</Tags>
    <Categories>Themes</Categories>
    <GalleryFlags>Public</GalleryFlags>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.80.0" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui,workspace" />
      <Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value="" />
      <Property Id="Microsoft.VisualStudio.Services.Content.Pricing" Value="Free"/>
    </Properties>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>
  </Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
  </Assets>
</PackageManifest>
""")
    (out / "[Content_Types].xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension=".json" ContentType="application/json"/>'
        '<Default Extension=".vsixmanifest" ContentType="text/xml"/></Types>\n')


# ------------------------------------------------------------------------- Zed
def hl(color, style=None, weight=None):
    d = {"color": color, "font_style": style, "font_weight": weight}
    return d


def zed_syntax():
    c, p = C, P
    k, s, f, t = c["keyword"], c["storage"], c["function"], c["type"]
    return {
        "comment": hl(c["comment"], "italic"),
        "comment.doc": hl(c["comment"], "italic"),
        "keyword": hl(k),
        "keyword.control": hl(k),
        "keyword.operator": hl(k),
        "keyword.import": hl(k),
        "keyword.declaration": hl(s),
        "keyword.definition": hl(s),
        "keyword.function": hl(s),
        "keyword.directive": hl(k),
        "keyword.preproc": hl(k),
        "keyword.jsdoc": hl(t, "italic"),
        "storageclass": hl(s),
        "type.qualifier": hl(k),
        "operator": hl(k),
        "preproc": hl(k),
        "tag": hl(k),
        "tag.jsx": hl(k),
        "tag.component.jsx": hl(t),
        "tag.doctype": hl(c["comment"]),
        "variable.special": hl(k, "italic"),
        "variable.builtin": hl(k, "italic"),
        "constant": hl(s),
        "constant.builtin": hl(s),
        "boolean": hl(s),
        "enum": hl(t),
        "variant": hl(s),
        "type.builtin": hl(s),
        "property.json_key": hl(s),
        "string.regex": hl(s),
        "string.special.symbol": hl(s),
        "function": hl(f),
        "function.method": hl(f),
        "function.call": hl(f),
        "function.builtin": hl(f),
        "function.decorator": hl(f),
        "function.special": hl(f),
        "function.definition": hl(f),
        "attribute": hl(f),
        "attribute.jsx": hl(f),
        "selector": hl(f),
        "selector.pseudo": hl(f),
        "type": hl(t),
        "type.class": hl(t),
        "type.interface": hl(t),
        "type.definition": hl(t),
        "type.jsdoc": hl(t, "italic"),
        "namespace": hl(t),
        "module": hl(t),
        "constructor": hl(s),
        "concept": hl(t),
        "lifetime": hl(c["param"], "italic"),
        "string": hl(c["string"]),
        "string.doc": hl(c["string"], "italic"),
        "string.special": hl(c["string"]),
        "string.special.path": hl(c["string"]),
        "text.literal": hl(c["string"]),
        "number": hl(c["number"]),
        "string.escape": hl(c["number"]),
        "embedded": hl(c["number"]),
        "punctuation.special": hl(c["number"]),
        "variable.parameter": hl(c["param"], "italic"),
        "variable.jsdoc": hl(c["param"], "italic"),
        "function.kwargs": hl(c["param"], "italic"),
        "label": hl(c["string"]),
        "variable": hl(c["var"]),
        "property": hl(c["property"]),
        "punctuation": hl(c["punct"]),
        "punctuation.bracket": hl(c["punct"]),
        "punctuation.delimiter": hl(c["punct"]),
        "punctuation.list_marker": hl(c["string"]),
        "punctuation.markup": hl(c["comment"]),
        "title": hl(k, None, 700),
        "title.markup": hl(k, None, 700),
        "emphasis": hl(c["number"], "italic"),
        "emphasis.strong": hl(c["string"], None, 700),
        "link_text": hl(t),
        "link_uri": hl(s),
        "diff.plus": hl(p["green"]),
        "diff.minus": hl(p["red"]),
        "diff.delta": hl(c["string"]),
        "hint": hl(c["comment"], "italic"),
        "predictive": hl("#585C88", "italic"),
        "primary": hl(c["var"]),
    }


def zed_style():
    u, p, c = UI, P, C
    st = {
        "accents": [c["string"], p["magenta"], p["cyan"], p["orange"], p["green"], p["blue"]],
        "background": u["panel"],
        "background.appearance": "opaque",
        "border": u["border"],
        "border.variant": "#171936",
        "border.focused": u["accent_dim"],
        "border.selected": u["accent_dim"],
        "border.transparent": "#00000000",
        "border.disabled": u["border"],
        "elevated_surface.background": u["raised"],
        "surface.background": u["panel"],
        "element.background": u["raised"],
        "element.hover": u["hover"],
        "element.active": u["select"],
        "element.selected": u["select"],
        "element.disabled": u["panel"],
        "drop_target.background": a(u["select"], "88"),
        "ghost_element.background": "#00000000",
        "ghost_element.hover": u["hover"],
        "ghost_element.active": u["select"],
        "ghost_element.selected": u["select"],
        "ghost_element.disabled": "#00000000",
        "text": u["fg"],
        "text.muted": u["fg_dim"],
        "text.placeholder": u["muted"],
        "text.disabled": "#585C88",
        "text.accent": p["cyan"],
        "icon": u["fg_dim"],
        "icon.muted": u["muted"],
        "icon.disabled": "#585C88",
        "icon.placeholder": u["muted"],
        "icon.accent": p["cyan"],
        "status_bar.background": u["panel"],
        "title_bar.background": u["panel"],
        "title_bar.inactive_background": u["deep"],
        "toolbar.background": u["bg"],
        "tab_bar.background": u["panel"],
        "tab.inactive_background": u["panel"],
        "tab.active_background": u["bg"],
        "search.match_background": a(c["string"], "40"),
        "search.active_match_background": a(c["string"], "70"),
        "panel.background": u["panel"],
        "panel.focused_border": u["accent_dim"],
        "panel.indent_guide": u["guide"],
        "panel.indent_guide_active": u["guide_active"],
        "panel.indent_guide_hover": u["guide_active"],
        "pane.focused_border": u["accent_dim"],
        "pane_group.border": u["border"],
        "scrollbar.thumb.background": a(u["select"], "88"),
        "scrollbar.thumb.hover_background": u["select"],
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.foreground": u["fg"],
        "editor.background": u["bg"],
        "editor.gutter.background": u["bg"],
        "editor.subheader.background": u["panel"],
        "editor.active_line.background": u["line"],
        "editor.highlighted_line.background": a(u["select"], "55"),
        "editor.line_number": "#41446E",
        "editor.active_line_number": u["fg_dim"],
        "editor.hover_line_number": u["fg"],
        "editor.invisible": "#2A2D51",
        "editor.wrap_guide": u["border"],
        "editor.active_wrap_guide": u["guide_active"],
        "editor.indent_guide": u["guide"],
        "editor.indent_guide_active": u["guide_active"],
        "editor.document_highlight.read_background": a(p["cyan"], "22"),
        "editor.document_highlight.write_background": a(p["cyan"], "38"),
        "editor.document_highlight.bracket_background": a(p["cyan"], "26"),
        "terminal.background": u["panel"],
        "terminal.foreground": u["fg"],
        "terminal.bright_foreground": u["fg_bright"],
        "terminal.dim_foreground": u["fg_dim"],
        "terminal.ansi.background": u["panel"],
        "link_text.hover": p["bright_cyan"],
        "version_control.added": p["green"],
        "version_control.modified": c["string"],
        "version_control.deleted": p["red"],
        "version_control.word_added": a(p["green"], "40"),
        "version_control.word_deleted": a(p["red"], "40"),
        "version_control.conflict_marker.ours": a(p["green"], "33"),
        "version_control.conflict_marker.theirs": a(p["blue"], "33"),
    }
    ansi = {
        "black": (p["lighter_background"], u["muted"], u["deep"]),
        "red": (p["red"], p["bright_red"], "#C53F5B"),
        "green": (p["green"], p["bright_green"], "#178839"),
        "yellow": (p["yellow"], p["bright_yellow"], "#917504"),
        "blue": (p["blue"], p["bright_blue"], "#4876C3"),
        "magenta": (p["magenta"], p["bright_magenta"], "#AC56BA"),
        "cyan": (p["cyan"], p["bright_cyan"], "#028397"),
        "white": (p["light_foreground"], p["bright_foreground"], u["fg_dim"]),
    }
    for name, (n, b, d) in ansi.items():
        st[f"terminal.ansi.{name}"] = n
        st[f"terminal.ansi.bright_{name}"] = b
        st[f"terminal.ansi.dim_{name}"] = d
    for status, color in [("conflict", p["magenta"]), ("created", p["green"]), ("deleted", p["red"]),
                          ("error", p["red"]), ("hidden", "#585C88"), ("hint", p["cyan"]),
                          ("ignored", "#585C88"), ("info", p["blue"]), ("modified", c["string"]),
                          ("predictive", "#585C88"), ("renamed", p["cyan"]), ("success", p["green"]),
                          ("unreachable", u["muted"]), ("warning", c["string"])]:
        st[status] = color
        st[f"{status}.background"] = a(color, "1a")
        st[f"{status}.border"] = a(color, "66")
    st["players"] = [
        {"cursor": p["bright_foreground"], "background": p["cyan"], "selection": a(u["select"], "cc")},
        {"cursor": p["magenta"], "background": p["magenta"], "selection": a(p["magenta"], "33")},
        {"cursor": c["string"], "background": c["string"], "selection": a(c["string"], "33")},
        {"cursor": p["green"], "background": p["green"], "selection": a(p["green"], "33")},
        {"cursor": p["orange"], "background": p["orange"], "selection": a(p["orange"], "33")},
        {"cursor": p["blue"], "background": p["blue"], "selection": a(p["blue"], "33")},
        {"cursor": p["red"], "background": p["red"], "selection": a(p["red"], "33")},
        {"cursor": p["cyan"], "background": p["cyan"], "selection": a(p["cyan"], "33")},
    ]
    st["syntax"] = zed_syntax()
    return st


def build_zed(out):
    out.mkdir(parents=True, exist_ok=True)
    family = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Edgerunners",
        "author": "Sothcheat",
        "themes": [{"name": "Edgerunners", "appearance": "dark", "style": zed_style()}],
    }
    (out / "edgerunners.json").write_text(json.dumps(family, indent=2) + "\n")


if __name__ == "__main__":
    build_vscode(HERE / "vscode")
    build_zed(HERE / "zed")
    print("wrote", HERE / "vscode", "and", HERE / "zed" / "edgerunners.json")
