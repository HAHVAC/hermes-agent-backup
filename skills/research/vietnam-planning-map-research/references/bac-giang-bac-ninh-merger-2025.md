# Bắc Giang & Bắc Ninh Administrative Merger (2025/2026)

From July 1, 2025 (under Resolution 1658/NQ-UBTVQH15), a major administrative reorganization merged parts/all of Bắc Giang and Bắc Ninh. This frequently causes discrepancies between map platforms (which may still use old provincial boundaries or paths) and reverse-geocoding APIs (like Nominatim/OSM, which update to the new boundaries).

## Reorganization of Huyện Hiệp Hòa (Bắc Giang cũ)

Huyện Hiệp Hòa (formerly of Bắc Giang province) was sáp nhập into the new **Tỉnh Bắc Ninh** and consolidated from 19 communes/towns into **4 large communes/wards** under **Thành phố Bắc Ninh**:

1. **Xã Hợp Thịnh**: Formed by merging the entire area and population of communes:
   - Thường Thắng
   - Mai Trung
   - Hùng Thái
   - Sơn Thịnh
   - Hợp Thịnh (old)

2. **Xã Hiệp Hòa**: Formed by merging the entire area and population of:
   - Thị trấn Thắng (former county seat)
   - Đông Lỗ
   - Đoan Bái
   - Danh Thắng
   - Lương Phong

3. **Xã Hoàng Vân**: Formed by merging the entire area and population of communes:
   - Đồng Tiến
   - Toàn Thắng
   - Ngọc Sơn
   - Hoàng Vân (old)

4. **Xã Xuân Cẩm**: Formed by merging the entire area and population of:
   - Thị trấn Bắc Lý
   - Hương Lâm
   - Mai Đình
   - Châu Minh
   - Xuân Cẩm (old)

## Impact on Planning & Real Estate Searches
- **URL Paths vs GPS Results:** Websites like `quyhoach24h.vn/bac-giang/` or Meey Map might group maps under `/bac-giang/`, but entering coordinates into geocoders will return address strings containing `Thành phố Bắc Ninh, Tỉnh Bắc Ninh`.
- **Search Queries:** When looking up planning decisions (e.g., KCN Hòa Phú, KĐT Châu Minh - Mai Đình, CCN Danh Thắng - Đoan Bái), query both the old names ("huyện Hiệp Hòa, tỉnh Bắc Giang") and new names ("xã Xuân Cẩm, tỉnh Bắc Ninh" or "xã Hiệp Hòa, tỉnh Bắc Ninh") as news and official documents span both eras.
