-- Edgerunners. A theme's hyprland.lua replaces the one Omarchy generates from
-- colors.toml, so the border gradient is repeated here; keep it in step with
-- hyprland_active_border there (the shell's popups and lock screen read that).

-- Focused window: Lucy cyan running into the violet of her rim light, a neon
-- edge. Others: dim indigo.
local active_border_color = { colors = { "rgb(0bafd7)", "rgb(bc48dd)" }, angle = 45 }
local inactive_border_color = "rgba(2b2d4faa)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },
})

-- Let the city show faintly through terminals.
o.window({ tag = "terminal" }, { opacity = "0.94 0.90" })
