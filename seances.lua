-- seances.lua — remplit le tableau d'accueil (Div #seances) avec TOUTES les séances :
--   en ligne (dossier seanceNN)  -> nom cliquable + « ✅ en ligne » (ou l'étiquette) ;
--   en préparation (_seanceNN)   -> nom en texte simple (SANS lien) + « 🚧 En préparation — … ».
-- L'étiquette « en préparation » vient de _seances-statut.yml (num: étiquette).

local function file_exists(p)
  local f = io.open(p, "r"); if f then f:close(); return true end; return false
end
local function esc(s)
  return (tostring(s):gsub("&","&amp;"):gsub("<","&lt;"):gsub(">","&gt;"))
end

-- étiquettes de statut
local statut = {}
do
  local mf = io.open("_seances-statut.yml", "r")
  if mf then
    for line in mf:lines() do
      if not line:match("^%s*#") then
        local n, lab = line:match("^%s*(%d+)%s*:%s*(.-)%s*$")
        if n and lab and lab ~= "" then
          lab = lab:gsub('^"(.*)"$', "%1"):gsub("^'(.*)'$", "%1")
          statut[tonumber(n)] = lab
        end
      end
    end
    mf:close()
  end
end

-- order + titre depuis un index.qmd
local function read_meta(path)
  local fh = io.open(path, "r"); if not fh then return nil end
  local seen, order, title = 0, nil, nil
  for line in fh:lines() do
    if line:match("^%-%-%-%s*$") then
      seen = seen + 1
      if seen >= 2 then break end
    else
      local o = line:match("^order:%s*(%d+)")
      if o then order = tonumber(o) end
      local nom = line:match('^nom:%s*"(.-)"')
      if nom then title = nom:match("%[(.-)%]") or nom end
    end
  end
  fh:close()
  return order, title
end

local function collect()
  local rows = {}
  for n = 1, 30 do
    local nn = string.format("%02d", n)
    local on_path  = "seances/seance"  .. nn .. "/index.qmd"
    local off_path = "seances/_seance" .. nn .. "/index.qmd"
    local path, is_on
    if file_exists(on_path) then path, is_on = on_path, true
    elseif file_exists(off_path) then path, is_on = off_path, false end
    if path then
      local order, title = read_meta(path)
      rows[#rows+1] = { nn = nn, order = order or n, title = title or ("Séance " .. n),
                        on = is_on, label = statut[n] }
    end
  end
  table.sort(rows, function(a, b) return a.order < b.order end)
  return rows
end

local function build_html(rows)
  local out = {
    '<style>.seances-table td,.seances-table th{vertical-align:middle}.seances-table .stx{color:#7a828c;font-style:italic}</style>',
    '<table class="table table-striped table-hover seances-table">',
    '<thead><tr><th>#</th><th>Séance</th><th>Correction</th></tr></thead><tbody>'
  }
  for _, r in ipairs(rows) do
    local name, corr
    if r.on then
      name = '<a href="seances/seance' .. r.nn .. '/index.html">' .. esc(r.title) .. '</a>'
      corr = r.label and ('<span class="stx">🔎 ' .. esc(r.label) .. '</span>') or '✅ en ligne'
    else
      name = '<span class="stx">' .. esc(r.title) .. '</span>'
      corr = '<span class="stx">🚧 En préparation' .. (r.label and (' — ' .. esc(r.label)) or '') .. '</span>'
    end
    out[#out+1] = '<tr><td>' .. r.order .. '</td><td>' .. name .. '</td><td>' .. corr .. '</td></tr>'
  end
  out[#out+1] = '</tbody></table>'
  return table.concat(out, "\n")
end

function Div(el)
  if el.identifier ~= "seances" then return nil end
  return pandoc.RawBlock("html", build_html(collect()))
end
