Duc Dung's Next.js blog (next-blog-vert.vercel.app) at C:\Users\Administrator\next-blog. GitHub: ducdung196qtr/next-blog. Vercel CLI deploy: npx vercel --token <TOKEN> --yes --prod from project root. Git push uses URL-embedded auth: https://ducdung196qtr:TOKEN@github.com/ducdung196qtr/next-blog.git. Skill `vercel-blog-auto-posting` has full dark-mode checklist (html.dark selector NOT nested in :root), image quality rules (w=1600 q=90), spacing rules, hero animation patterns, and all pitfalls.
§
Rất khó tính về UI: dark mode phải mượt (đã từ chối web vì dark mode không hoạt động), ảnh phải sắc nét 1600px, spacing phải rộng, hero phải có animation ấn tượng. Khi gặp lỗi UI muốn fix luôn, không thích agent đoán mò — cần verify thực tế (chụp ảnh màn hình hoặc fetch CSS deployed).
§
Từng reject footer "Powered by Vercel & Next.js" — footer phải là thương hiệu riêng. Từng reject author "NewsPress AI" — tác giả luôn là "Đức Dũng". Từng reject màu đỏ #e63946 — thích xanh dương #1a56db + vàng gold.
§
PHẢI HỎI trước khi viết bài blog, deploy, hay sửa nội dung web. User đã nhắc 3 lần: "nào làm gì phải hỏi ý kiến tôi đã chứ", "từ từ. ai bảo mà làm", "nhớ đấy. sau phải hỏi tôi". Luôn trình bày kế hoạch + options rồi đợi xác nhận. Ngoại lệ duy nhất: khi user nói "làm đi" / "cứ làm".
§
Video TikTok pipeline: mọi rule trong skill social-video-rendering. Audio-first sync, 62/38 split, Deconstructed style, preview trước render, báo 10%, KHÔNG tự ý đổi audio đã duyệt.
§
Edge TTS library hay chết → fallback Hermes text_to_speech tool. gTTS Google bị reject. Không tự ý cài FPT.AI/ElevenLabs khi chưa hỏi.