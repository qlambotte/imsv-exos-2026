-- Rendu « carte » des méthodes de la boîte à outils, à partir d'une SOURCE UNIQUE,
-- en HTML (site) et en typst (PDF imprimable). Chaque méthode s'écrit :
--
--   ::: {.methode obj="O1" titre="Traduire une phrase en langage formel"}
--   ::: {.quand}   … :::
--   ::: {.etapes}  liste numérotée :::
--   ::: {.exemple} … :::
--   ::: {.piege}   … :::
--   :::
--
-- HTML : « Quand l'utiliser » reste visible ; les réponses (Étapes · Exemple ·
--        Piège) sont dans un volet REPLIÉ par défaut (« construis d'abord »).
-- PDF  : tout est affiché, UNE méthode par page. Les libellés sont ajoutés
--        automatiquement ; le contenu reste du Markdown normal (maths comprises).

local LABELS = {
  quand   = "Quand l'utiliser ?",
  etapes  = "Étapes",
  exemple = "Exemple",
  piege   = "Le piège",
}
local ORDER = { "quand", "etapes", "exemple", "piege" }
local REPONSES = { etapes = true, exemple = true, piege = true }  -- repliées en HTML

local mcount = 0   -- pour les sauts de page (PDF), réinitialisé à chaque rendu

local function has_class(el, name)
  for _, c in ipairs(el.classes) do if c == name then return true end end
  return false
end

function Div(el)
  if not has_class(el, "methode") then return nil end
  local titre = el.attributes.titre or ""
  local obj   = el.attributes.obj or ""

  local sect = {}
  for _, blk in ipairs(el.content) do
    if blk.t == "Div" then
      for key, _ in pairs(LABELS) do
        if has_class(blk, key) then sect[key] = blk.content end
      end
    end
  end

  local out = {}

  if quarto.doc.is_format("typst") then
    mcount = mcount + 1
    if mcount > 1 then out[#out + 1] = pandoc.RawBlock("typst", "#pagebreak(weak: true)") end
    out[#out + 1] = pandoc.RawBlock("typst", '#methodecard("' .. titre .. '", "' .. obj .. '")[')
    for _, key in ipairs(ORDER) do
      if sect[key] then
        out[#out + 1] = pandoc.RawBlock("typst", '#msect("' .. LABELS[key] .. '")[')
        for _, b in ipairs(sect[key]) do out[#out + 1] = b end
        out[#out + 1] = pandoc.RawBlock("typst", ']')
      end
    end
    out[#out + 1] = pandoc.RawBlock("typst", ']')
    return out
  end

  -- HTML
  local function emit_sect(key)
    out[#out + 1] = pandoc.RawBlock("html",
      '<div class="mc-sect mc-' .. key .. '"><div class="mc-label">' .. LABELS[key] .. '</div>')
    for _, b in ipairs(sect[key]) do out[#out + 1] = b end
    out[#out + 1] = pandoc.RawBlock("html", '</div>')
  end

  out[#out + 1] = pandoc.RawBlock("html",
    '<div class="methode-card"><div class="mc-head"><span class="mc-titre">' .. titre ..
    '</span><span class="mc-badge">' .. obj .. '</span></div><div class="mc-body">')

  -- sections visibles (avant le volet)
  for _, key in ipairs(ORDER) do
    if sect[key] and not REPONSES[key] then emit_sect(key) end
  end

  -- volet replié : les réponses
  local has_rep = false
  for _, key in ipairs(ORDER) do if sect[key] and REPONSES[key] then has_rep = true end end
  if has_rep then
    out[#out + 1] = pandoc.RawBlock("html",
      '<details class="mc-reponses"><summary>Déplier le corrigé — étapes, exemple, piège</summary>')
    for _, key in ipairs(ORDER) do
      if sect[key] and REPONSES[key] then emit_sect(key) end
    end
    out[#out + 1] = pandoc.RawBlock("html", '</details>')
  end

  out[#out + 1] = pandoc.RawBlock("html", '</div></div>')
  return out
end

function Pandoc(doc)
  if quarto.doc.is_format("typst") then
    table.insert(doc.blocks, 1, pandoc.RawBlock("typst", [[
#let methodecard(titre, obj, body) = block(width:100%, above:0pt, below:0pt, breakable:true, stroke:0.7pt+rgb("#c7d6ea"), radius:5pt, inset:0pt, clip:true)[
  #block(width:100%, inset:(x:12pt, y:9pt), fill:rgb("#eef3fb"), below:0pt)[
    #grid(columns:(1fr,auto), column-gutter:8pt, align:(left+horizon, right+horizon),
      text(size:14pt, weight:700, fill:rgb("#1f3a5f"), titre),
      box(inset:(x:8pt,y:3pt), radius:3pt, fill:rgb("#dbe6f6"), text(size:9.5pt, weight:700, fill:rgb("#2f4f7a"), obj)))
  ]
  #block(width:100%, inset:(x:12pt, y:11pt))[#body]
]
#let msect(label, body) = block(width:100%, above:10pt, below:0pt, breakable:false)[
  #text(size:9.5pt, weight:700, fill:rgb("#2f6fb0"), upper(label))
  #v(2pt)
  #body
]
]]))
  end
  return doc
end
