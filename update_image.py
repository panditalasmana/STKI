import pandas as pd

df = pd.read_csv("dataset/laptop_dataset.csv")

def get_image(nama):
    nama_lower = nama.lower().strip()
    
    # ==================== ASUS ====================
    if "rog strix" in nama_lower or "rog scar" in nama_lower:
        return "https://images.unsplash.com/photo-1603302576837-37561b2e2302?q=80&w=1200&auto=format&fit=crop"
    elif "rog zephyrus" in nama_lower or "rog flow" in nama_lower or "rog duo" in nama_lower:
        return "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=1200&auto=format&fit=crop"
    elif "tuf" in nama_lower:
        return "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=1200&auto=format&fit=crop"
    elif "zenbook" in nama_lower or "expertbook" in nama_lower or "proart" in nama_lower:
        return "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?q=80&w=1200&auto=format&fit=crop"
    elif "vivobook" in nama_lower:
        return "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== LENOVO ====================
    elif "legion" in nama_lower:
        return "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1200&auto=format&fit=crop"
    elif "loq" in nama_lower:
        return "https://images.unsplash.com/photo-1588702547923-7093a6c3a3e4?q=80&w=1200&auto=format&fit=crop"
    elif "yoga" in nama_lower:
        return "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?q=80&w=1200&auto=format&fit=crop"
    elif "ideapad" in nama_lower or "thinkpad" in nama_lower:
        return "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== ACER ====================
    elif "predator" in nama_lower or "helios" in nama_lower:
        return "https://images.unsplash.com/photo-1517430816045-df4b7de11d1d?q=80&w=1200&auto=format&fit=crop"
    elif "nitro" in nama_lower:
        return "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=1200&auto=format&fit=crop"
    elif "swift" in nama_lower:
        return "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?q=80&w=1200&auto=format&fit=crop"
    elif "aspire" in nama_lower:
        return "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== MSI ====================
    elif "raider" in nama_lower or "titan" in nama_lower:
        return "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?q=80&w=1200&auto=format&fit=crop"
    elif "katana" in nama_lower or "sword" in nama_lower or "crosshair" in nama_lower:
        return "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?q=80&w=1200&auto=format&fit=crop"
    elif "prestige" in nama_lower or "summit" in nama_lower or "creator" in nama_lower:
        return "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?q=80&w=1200&auto=format&fit=crop"
    elif "thin" in nama_lower or "modern" in nama_lower:
        return "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== DELL ====================
    elif "alienware" in nama_lower:
        return "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?q=80&w=1200&auto=format&fit=crop"
    elif "xps" in nama_lower:
        return "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=1200&auto=format&fit=crop"
    elif "inspiron" in nama_lower:
        return "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1200&auto=format&fit=crop"
    elif "latitude" in nama_lower or "precision" in nama_lower:
        return "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== HP ====================
    elif "omen" in nama_lower or "victus" in nama_lower:
        return "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=1200&auto=format&fit=crop"
    elif "spectre" in nama_lower or "envy" in nama_lower:
        return "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?q=80&w=1200&auto=format&fit=crop"
    elif "pavilion" in nama_lower:
        return "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== APPLE ====================
    elif "macbook" in nama_lower or "apple" in nama_lower:
        return "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?q=80&w=1200&auto=format&fit=crop"
    
    # ==================== LAINNYA ====================
    elif "razer" in nama_lower:
        return "https://images.unsplash.com/photo-1611078489935-0cb964de46d6?q=80&w=1200&auto=format&fit=crop"
    elif "samsung" in nama_lower:
        return "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?q=80&w=1200&auto=format&fit=crop"
    
    # Default
    else:
        return "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1200&auto=format&fit=crop"


# Terapkan ke dataset
df["image"] = df["nama_laptop"].apply(get_image)

# Simpan
df.to_csv("dataset/laptop_dataset.csv", index=False)

print("✅ Gambar telah diupdate dengan detail merk + tipe!")
print(f"Total laptop: {len(df)}")