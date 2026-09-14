-- Filtre IMSV :
--  (1) NUMÉROTE AUTOMATIQUEMENT les exercices, par catégorie, dans l'ordre du
--      document, et met en forme le titre. Titre source :
--         « Exercice|Catégorie|niveau|Objectif »   (PAS de numéro à la main)
--      Rendu : « ✎ Exercice S.1   …   Catégorie · Ox · ★★☆ ». Le préfixe vient de
--      la catégorie : Socle→S, Transfert→T, Renforcement→R, Dépassement→D,
--      Complément→C (sinon 1re lettre). Le compteur repart à chaque rendu de
--      document : réordonner les exercices les renumérote tout seul.
--      En HTML : ancre #exercice-<S1> + petit lien « # ». (Un ancien « Exercice 5|… »
--      reste toléré : le numéro écrit est ignoré.)
--  (2) « énoncés seuls » (IMSV_ENONCES=1) : retire les aides et les callouts
--      non-exercice (sauf les consignes « tip »).
--  (3) AIDES en PDF « complet » (typst) : convertit les onglets (indice /
--      solution / piège) en boîtes légères à filet de couleur, fond blanc, titre
--      en gras coloré (« Indice 1 », pas « INDICE 1 »). En HTML, les onglets
--      (.panel-tabset) sont laissés intacts.

local SYMBOLE = "✎"
local counters = {}   -- compteur par préfixe, pour la durée d'un rendu de document
local PREFIX = {
  ["Socle"] = "S", ["Transfert"] = "T",
  ["Renforcement"] = "R", ["Dépassement"] = "D", ["Complément"] = "C",
}

local function stars(n)
  n = math.floor(tonumber(n) or 1)
  if n < 1 then n = 1 end
  if n > 3 then n = 3 end
  return string.rep("★", n) .. string.rep("☆", 3 - n)
end

local function trim(s) return (s:gsub("^%s+", ""):gsub("%s+$", "")) end

function Callout(el)
  local t = pandoc.utils.stringify(el.title or "")
  local after = t:match("^Exercice%s*(.-)%s*$")
  local cat, niv, obj
  if after then
    after = after:gsub("^%d+%s*", ""):gsub("^|%s*", "")   -- tolère un ancien numéro / pipe de tête
    cat, niv, obj = after:match("^([^|]+)|(%d+)|([^|]+)$")
    if not cat then cat, niv = after:match("^([^|]+)|(%d+)$") end
  end
  if cat then
    cat = trim(cat)
    local p = PREFIX[cat] or cat:sub(1, 1):upper()
    counters[p] = (counters[p] or 0) + 1
    local numstr = p .. "." .. counters[p]
    local right = cat .. (obj and (" · " .. obj) or "") .. " · " .. stars(niv)
    local title = {
      pandoc.Str(SYMBOLE), pandoc.Space(),
      pandoc.Strong({ pandoc.Str("Exercice"), pandoc.Space(), pandoc.Str(numstr) }),
    }
    if quarto.doc.is_format("typst") then
      table.insert(title, pandoc.RawInline("typst", "#h(1fr) "))
      table.insert(title, pandoc.Str(right))
    else
      local id = "exercice-" .. p .. counters[p]
      table.insert(title, 1, pandoc.RawInline("html", '<span class="exo-anchor" id="' .. id .. '"></span>'))
      table.insert(title, pandoc.RawInline("html", ' <a class="exo-hash" href="#' .. id .. '" title="Lien vers cet exercice">#</a>'))
      table.insert(title, pandoc.RawInline("html", '<span class="exo-meta">' .. right .. '</span>'))
    end
    el.title = title
    el.icon = false
    return el
  end

  if os.getenv("IMSV_ENONCES") == "1" and el.type ~= "tip" then
    return {}
  end
  return el
end

-- Couleur du filet selon l'onglet d'aide.
local function aide_color(label)
  local l = label:lower()
  if l:find("indice") then return "#2f6fb0"       -- bleu
  elseif l:find("solution") then return "#2e7d46" -- vert
  elseif l:find("pi") then return "#b5561f"        -- ambre (piège)
  else return "#555555" end
end

function Div(el)
  local is_aide = false
  for _, c in ipairs(el.classes) do if c == "aides" then is_aide = true end end

  if os.getenv("IMSV_ENONCES") == "1" then
    for _, c in ipairs(el.classes) do
      if c == "aides" or c == "panel-tabset" then return {} end
    end
    return el
  end

  -- PDF « complet » : transformer les onglets d'aide en boîtes à filet coloré.
  if is_aide and quarto.doc.is_format("typst") then
    local tab = el.content[1]
    if tab and tab.attributes and tab.attributes.__quarto_custom_type == "Tabset" then
      local sc, out = tab.content, {}
      local k = 1
      while k <= #sc do
        local body, titleblk = sc[k], sc[k + 1]   -- scaffolds par paires : [contenu, titre]
        if titleblk then
          local label = trim(pandoc.utils.stringify(titleblk))
          out[#out + 1] = pandoc.RawBlock("typst",
            '#aidebox("' .. label .. '", rgb("' .. aide_color(label) .. '"))[')
          if body and body.content then
            for _, b in ipairs(body.content) do out[#out + 1] = b end
          end
          out[#out + 1] = pandoc.RawBlock("typst", "]")
        end
        k = k + 2
      end
      el.content = out
    end
    return el
  end

  return el
end

function Pandoc(doc)
  if quarto.doc.is_format("typst") then
    table.insert(doc.blocks, 1, pandoc.RawBlock("typst", "#let fa-fire = () => none"))
    table.insert(doc.blocks, 1, pandoc.RawBlock("typst",
      '#let aidebox(label, col, body) = block(width:100%, above:7pt, below:0pt, breakable:false, ' ..
      'stroke: 0.6pt + col, radius: 3pt, inset: (x:9pt, y:7pt), fill: white)[' ..
      '#text(size:0.9em, weight:700, fill:col)[#label] #v(2pt) #body]'))
  end
  return doc
end
