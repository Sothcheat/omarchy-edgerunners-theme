-- Edgerunners Neovim: Omarchy's generated aether setup plus the shared editor syntax.
return {
  {
    "bjarneo/aether.nvim",
    branch = "v3",
    name = "aether",
    priority = 1000,
    opts = {
      -- Edgerunners syntax, shared with the VS Code and Zed themes
      -- (editors/build.py): One Monokai's structure, where every role has its
      -- own hue, in Edgerunners colours. Nothing bold.
      --   keywords, operators, tags   neon red
      --   declaration words (function, class, interface), built-in types,
      --     constants, booleans       Lucy cyan
      --   functions, attributes       acid green
      --   classes, types, modules     Lucy blue
      --   strings                     rocket gold
      --   numbers, escapes            neon violet
      --   parameters                  HOTEL orange, italic
      --   self / this                 neon red, italic
      --   properties, object keys     neon pink
      --   variables                   lavender white
      styles = {
        comments = { italic = true },
        keywords = {},
        functions = {},
        variables = {},
      },
      on_highlights = function(hl, c)
        local keyword = { fg = c.red }
        local storage = { fg = c.cyan }
        local func = { fg = c.green }
        local type = { fg = c.blue }
        local str = { fg = c.yellow }
        local number = { fg = c.magenta }
        local param = { fg = c.orange, italic = true }
        local self = { fg = c.red, italic = true }
        local plain = { fg = c.fg }
        local prop = { fg = "#FE8CC5" }
        local punct = { fg = c.dark_fg }

        local function set(groups, style)
          for _, g in ipairs(groups) do
            hl[g] = style
          end
        end

        set({ "Keyword", "Statement", "Conditional", "Repeat", "Exception", "Include", "StorageClass",
          "PreProc", "Define", "Macro", "Operator", "@keyword", "@keyword.return", "@keyword.import",
          "@keyword.conditional", "@keyword.repeat", "@keyword.exception", "@keyword.modifier",
          "@keyword.operator", "@keyword.coroutine", "@keyword.directive", "@type.qualifier", "@operator",
          "@tag", "@tag.tsx", "@tag.javascript", "@tag.builtin" }, keyword)
        set({ "Structure", "Typedef", "@keyword.function", "@keyword.type", "@keyword.storage",
          "Constant", "Boolean", "@constant", "@constant.builtin", "@boolean", "@type.builtin",
          "@string.regexp", "@string.special.symbol", "@lsp.type.enumMember" }, storage)
        set({ "Function", "@function", "@function.call", "@function.method", "@function.method.call",
          "@function.builtin", "@function.macro", "@constructor", "@attribute", "@attribute.builtin",
          "@tag.attribute", "@lsp.type.function", "@lsp.type.method", "@lsp.type.decorator" }, func)
        set({ "Type", "@type", "@type.definition", "@module", "@module.builtin", "@lsp.type.type",
          "@lsp.type.class", "@lsp.type.interface", "@lsp.type.enum", "@lsp.type.namespace",
          "@lsp.type.typeParameter", "@constructor.tsx" }, type)
        set({ "String", "Character", "@string", "@character", "@label", "@markup.list" }, str)
        hl["@string.documentation"] = { fg = c.yellow, italic = true }
        set({ "Number", "Float", "@number", "@number.float", "@string.escape", "@character.special",
          "@punctuation.special", "SpecialChar" }, number)
        set({ "@variable.parameter", "@variable.parameter.builtin", "@lsp.type.parameter" }, param)
        set({ "@variable.builtin", "@lsp.typemod.variable.defaultLibrary" }, self)
        set({ "Identifier", "@variable", "@lsp.type.variable" }, plain)
        set({ "@variable.member", "@property", "@lsp.type.property" }, prop)
        set({ "Delimiter", "@punctuation", "@punctuation.bracket", "@punctuation.delimiter",
          "@tag.delimiter" }, punct)
        hl.Special = storage
        hl["@markup.heading"] = { fg = c.red, bold = true }
        hl["@markup.link"], hl["@markup.link.url"] = type, storage
        hl["@markup.raw"] = storage
      end,
      colors = {
        bg = "#0B0C24",
        dark_bg = "#06071A",
        darker_bg = "#030310",
        lighter_bg = "#141534",

        fg = "#DDDDF7",
        dark_fg = "#A0A2C1",
        light_fg = "#C3C4E1",
        bright_fg = "#F2F2FE",
        muted = "#717AAA",

        red = "#FE5F7E",
        yellow = "#CBA501",
        orange = "#ED734D",
        green = "#06AE46",
        cyan = "#05A5BF",
        blue = "#5A96F9",
        magenta = "#D869EA",
        brown = "#A37A52",

        bright_red = "#FEA6BE",
        bright_yellow = "#F1E607",
        bright_green = "#41D968",
        bright_cyan = "#03D1EA",
        bright_blue = "#9CBFFE",
        bright_magenta = "#F5A1F9",

        accent = "#FE5F7E",
        cursor = "#F2F2FE",
        foreground = "#DDDDF7",
        background = "#0B0C24",
        selection = "#003A56",
        selection_foreground = "#F2F2FE",
        selection_background = "#003A56",
      },
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "aether",
    },
  },
}
