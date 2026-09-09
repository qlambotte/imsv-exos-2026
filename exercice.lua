-- Filtre IMSV :
--  (1) met en forme le titre des exercices « Exercice N|Catégorie|niveau »
--      en « ✎ Exercice N  <hfill>  Catégorie · ★★☆ », sans icône d'info.
--      En HTML, pose une ANCRE (#exercice-N) pour pointer un exercice, avec un
--      petit lien « # » visible au survol. Le rendu Typst (PDF) est INCHANGÉ.
--  (2) version « énoncés seuls » (IMSV_ENONCES=1) : retire les aides (.aides) et
--      tout callout qui n'est pas un exercice (sauf les consignes « tip »).

local SYMBOLE = "✎"

local function stars(n)
  n = math.floor(tonumber(n) or 1)
  if n < 1 then n = 1 end
  if n > 3 then n = 3 end
  return string.rep("★", n) .. string.rep("☆", 3 - n)
end

function Callout(el)
  local t = pandoc.utils.stringify(el.title or "")
  -- Titre : « Exercice N|Catégorie|niveau » ou « Exercice N|Catégorie|niveau|Objectif »
  local num, cat, niv, obj = t:match("^Exercice%s+([^|]+)|([^|]+)|(%d+)|([^|]+)%s*$")
  if not num then
    num, cat, niv = t:match("^Exercice%s+([^|]+)|([^|]+)|(%d+)%s*$")
  end
  if num then
    local right = cat .. (obj and (" · " .. obj) or "") .. " · " .. stars(niv)
    local title = {
      pandoc.Str(SYMBOLE), pandoc.Space(),
      pandoc.Strong({ pandoc.Str("Exercice"), pandoc.Space(), pandoc.Str(num) }),
    }
    if quarto.doc.is_format("typst") then
      -- Rendu PDF : identique à l'existant (aucune ancre)
      table.insert(title, pandoc.RawInline("typst", "#h(1fr) "))
      table.insert(title, pandoc.Str(right))
    else
      -- Rendu HTML : ancre + petit lien « # » + méta à droite
      local id = "exercice-" .. num:gsub("%s+", "")
      table.insert(title, 1, pandoc.RawInline("html", '<span class="exo-anchor" id="' .. id .. '"></span>'))
      table.insert(title, pandoc.RawInline("html", ' <a class="exo-hash" href="#' .. id .. '" title="Lien vers cet exercice">#</a>'))
      table.insert(title, pandoc.RawInline("html", '<span class="exo-meta">' .. right .. '</span>'))
    end
    el.title = title
    el.icon = false
    return el
  end

  -- version « énoncés seuls » : on retire tout callout non-exercice, sauf les consignes (tip)
  if os.getenv("IMSV_ENONCES") == "1" and el.type ~= "tip" then
    return {}
  end
  return el
end

-- Les aides vivent dans un bloc  ::: {.aides} contenant un panel-tabset.
-- Version « énoncés seuls » : on retire tout le bloc d'aides.
function Div(el)
  if os.getenv("IMSV_ENONCES") == "1" then
    for _, c in ipairs(el.classes) do
      if c == "aides" or c == "panel-tabset" then
        return {}
      end
    end
  end
  return el
end

-- Réglage Typst factorisé : Quarto ignore « icon=false » sur les callouts en Typst ;
-- on neutralise l'icône de type des exercices (callout « caution »).
function Pandoc(doc)
  if quarto.doc.is_format("typst") then
    table.insert(doc.blocks, 1, pandoc.RawBlock("typst", "#let fa-fire = () => none"))
  end
  return doc
end
