#!/usr/bin/env python3
"""
AI TEXT TO HUMAN TEXT CONVERTER
================================
Program untuk mengkonversi tulisan buatan AI menjadi tulisan yang lebih natural dan manusiawi.

Fitur:
✓ Menghapus kalimat yang terlalu formal
✓ Menambahkan variasi kalimat
✓ Menambahkan kata-kata transisi natural
✓ Mengubah struktur kalimat yang repetitif
✓ Menambahkan kontraksi dan ungkapan informal
✓ Analisis tingkat "kemanusiaan" teks
"""

import re
import random
from collections import Counter
from typing import List, Tuple

class AItoHumanConverter:
    """Mengkonversi teks buatan AI menjadi teks yang lebih manusiawi"""
    
    def __init__(self):
        # Dictionary untuk mengganti kata-kata formal dengan informal
        self.formal_to_informal = {
            'oleh karena itu': random.choice(['jadi', 'makanya', 'karena itu']),
            'dengan demikian': random.choice(['dengan begitu', 'jadi', 'dengan cara ini']),
            'namun demikian': random.choice(['tapi', 'meskipun begitu', 'tapi tetap saja']),
            'sebaliknya': random.choice(['malah', 'justru', 'sebaliknya']),
            'hendaknya': 'harusnya',
            'sesungguhnya': 'sebenarnya',
            'tidaklah': 'nggak',
            'bukanlah': 'bukan',
            'sungguh': 'banget',
            'benar-benar': 'bener-bener',
            'sangat': random.choice(['banget', 'sekali', 'parah']),
            'mungkin': random.choice(['kayaknya', 'mungkin', 'sepertinya']),
            'dapat': random.choice(['bisa', 'bisa', 'bisa']),
            'akan': random.choice(['bakal', 'akan', 'akan']),
            'di antara': 'antara',
            'sejak': 'dari',
            'mengingat': 'karena',
            'bilamana': 'kalau',
        }
        
        # Kata-kata transisi natural
        self.transition_words = [
            'sih', 'loh', 'nih', 'kan', 'deh', 'dong', 'tuh', 'itu',
            'nah', 'terus', 'jadi', 'jadi gini', 'yang jelas', 'yang penting',
            'pokoknya', 'gampang', 'gitu deh', 'gimana ya', 'kira-kira'
        ]
        
        # Kata-kata pengisi yang membuat teks lebih manusiawi
        self.filler_words = [
            'sih', 'lah', 'kan', 'dong', 'nih', 'loh', 'tuh'
        ]
        
        # Ungkapan informal untuk pengganti
        self.phrase_replacements = {
            'hal ini menunjukkan': 'ini menunjukkan kalau',
            'oleh sebab itu': 'jadi',
            'untuk alasan ini': 'karena itu',
            'pada akhirnya': 'akhirnya',
            'dalam hal ini': 'dalam hal ini',
            'perlu diketahui bahwa': 'yang penting diketahui adalah',
            'dapat ditarik kesimpulan': 'bisa disimpulin',
            'hasil penelitian menunjukkan': 'hasilnya menunjukkin kalau',
            'berdasarkan hasil analisis': 'berdasarkan analisisnya',
            'diperoleh informasi bahwa': 'didapat info kalau',
        }
    
    def remove_repetitive_patterns(self, text: str) -> str:
        """Menghapus pola kalimat yang repetitif"""
        # Hapus kalimat-kalimat yang terlalu sering diulang
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Cek untuk pola repetitif
        seen_patterns = set()
        result = []
        
        for sentence in sentences:
            # Extract pola dasar kalimat
            pattern = self._extract_pattern(sentence)
            
            if pattern not in seen_patterns:
                result.append(sentence)
                seen_patterns.add(pattern)
            else:
                # Variasikan kalimat jika sudah ada yang serupa
                new_sentence = self._rephrase_sentence(sentence)
                if new_sentence:
                    result.append(new_sentence)
        
        return ' '.join(result)
    
    def _extract_pattern(self, sentence: str) -> str:
        """Ekstrak pola dasar dari kalimat"""
        # Ambil 2-3 kata pertama sebagai pola
        words = sentence.split()[:3]
        return ' '.join(words).lower()
    
    def _rephrase_sentence(self, sentence: str) -> str:
        """Ubah struktur kalimat"""
        # Ini adalah contoh sederhana
        return sentence
    
    def add_informal_touches(self, text: str) -> str:
        """Tambahkan sentuhan informal ke teks"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        result = []
        
        for sentence in sentences:
            # Tambahkan kata-kata pengisi dengan probabilitas tertentu
            if random.random() < 0.2:  # 20% chance
                filler = random.choice(self.filler_words)
                # Insert di tengah-tengah kalimat
                words = sentence.rstrip('.!?').split()
                if len(words) > 3:
                    insert_pos = random.randint(1, len(words)-1)
                    words.insert(insert_pos, filler + ',')
                sentence = ' '.join(words)
            
            result.append(sentence)
        
        return ' '.join(result)
    
    def replace_formal_words(self, text: str) -> str:
        """Ganti kata-kata formal dengan informal"""
        result = text
        
        # Ganti phrase terlebih dahulu (lebih panjang)
        for formal, informal in self.phrase_replacements.items():
            result = re.sub(r'\b' + formal + r'\b', informal, result, flags=re.IGNORECASE)
        
        # Ganti individual words
        for formal, informal in self.formal_to_informal.items():
            result = re.sub(r'\b' + formal + r'\b', informal, result, flags=re.IGNORECASE)
        
        return result
    
    def vary_sentence_structure(self, text: str) -> str:
        """Variasikan struktur kalimat"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        result = []
        
        for i, sentence in enumerate(sentences):
            # Setiap beberapa kalimat, ubah struktur sedikit
            if i % 3 == 0 and len(sentence) > 50:
                # Potong kalimat panjang menjadi dua
                words = sentence.split()
                mid = len(words) // 2
                sentence = ' '.join(words[:mid]) + '. ' + ' '.join(words[mid:])
            
            result.append(sentence)
        
        return ' '.join(result)
    
    def remove_overuse_of_certain_words(self, text: str) -> str:
        """Hapus penggunaan kata tertentu yang berlebihan"""
        words = text.split()
        word_count = Counter(words)
        
        # Kata-kata yang sering digunakan AI dan harus dikurangi
        overused_words = {
            'adalah': 0.3,  # Kurangi hingga 30% dari kemunculan
            'yang': 0.4,
            'dapat': 0.3,
            'dalam': 0.35,
            'terdapat': 0.4,
            'memiliki': 0.35,
        }
        
        result = []
        word_reduce_count = {word: 0 for word in overused_words}
        
        for word in words:
            word_lower = word.lower().rstrip('.,!?;:')
            
            if word_lower in overused_words:
                # Hitungkan berapa banyak kata ini muncul
                total_occurrences = word_count[word]
                target_reduction = int(total_occurrences * (1 - overused_words[word_lower]))
                
                if word_reduce_count[word_lower] < target_reduction:
                    result.append(word)
                    word_reduce_count[word_lower] += 1
                # Skip jika sudah mencapai target pengurangan
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def add_contractions(self, text: str) -> str:
        """Tambahkan kontraksi Indonesia yang natural"""
        contractions = {
            r'\btidak\s+akan\b': "bakal nggak",
            r'\btidak\s+bisa\b': "nggak bisa",
            r'\btidak\s+ada\b': "nggak ada",
            r'\bkamu\s+adalah\b': "kamu itu",
            r'\bsaya\s+adalah\b': "saya itu",
            r'\bdia\s+adalah\b': "dia itu",
        }
        
        result = text
        for pattern, contraction in contractions.items():
            result = re.sub(pattern, contraction, result, flags=re.IGNORECASE)
        
        return result
    
    def analyze_humanness(self, text: str) -> dict:
        """Analisis tingkat 'kemanusiaan' teks"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        words = text.split()
        
        metrics = {}
        
        # 1. Hitung rata-rata panjang kalimat (human: 15-25 kata)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        metrics['avg_sentence_length'] = avg_sentence_length
        metrics['sentence_variety'] = self._calculate_sentence_variety(sentences)
        
        # 2. Hitung penggunaan kata-kata formal
        formal_words_count = sum(1 for word in words if any(
            re.search(r'\b' + formal + r'\b', word, re.IGNORECASE) 
            for formal in self.formal_to_informal.keys()
        ))
        metrics['formal_words_ratio'] = formal_words_count / len(words) if words else 0
        
        # 3. Hitung penggunaan kata pengisi (transisi) - lebih tinggi = lebih manusiawi
        filler_count = sum(1 for word in words if word.lower() in self.filler_words)
        metrics['filler_words_ratio'] = filler_count / len(words) if words else 0
        
        # 4. Hitung kontraksi
        contraction_count = len(re.findall(r"\b(nggak|gak|itu|sih|dong|kan)\b", text, re.IGNORECASE))
        metrics['contraction_count'] = contraction_count
        
        # 5. Skor kemanusiaan keseluruhan (0-100)
        humanness_score = self._calculate_humanness_score(metrics)
        metrics['humanness_score'] = humanness_score
        
        return metrics
    
    def _calculate_sentence_variety(self, sentences: List[str]) -> float:
        """Hitung variasi struktur kalimat"""
        if len(sentences) < 2:
            return 0
        
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        
        # Hitung variance
        variance = sum((x - avg_length) ** 2 for x in lengths) / len(lengths)
        
        # Normalisasi ke 0-1
        return min(variance / 100, 1.0)
    
    def _calculate_humanness_score(self, metrics: dict) -> int:
        """Hitung skor kemanusiaan 0-100"""
        score = 50  # Base score
        
        # Sentence length (ideal 15-25 kata)
        avg_len = metrics['avg_sentence_length']
        if 15 <= avg_len <= 25:
            score += 20
        elif 12 <= avg_len <= 30:
            score += 10
        
        # Sentence variety
        score += int(metrics['sentence_variety'] * 20)
        
        # Formal words (lebih sedikit = lebih baik)
        formal_ratio = metrics['formal_words_ratio']
        if formal_ratio < 0.05:
            score += 15
        elif formal_ratio < 0.1:
            score += 10
        elif formal_ratio < 0.15:
            score += 5
        
        # Filler words (sedikit = lebih natural)
        filler_ratio = metrics['filler_words_ratio']
        if 0.01 <= filler_ratio <= 0.05:
            score += 10
        elif filler_ratio < 0.01:
            score += 5
        
        return min(max(score, 0), 100)
    
    def convert(self, text: str) -> str:
        """Konversi teks AI menjadi teks manusiawi"""
        print("[*] Memproses teks...")
        
        # Langkah-langkah konversi
        print("[1] Menghapus pola repetitif...")
        text = self.remove_repetitive_patterns(text)
        
        print("[2] Mengganti kata-kata formal...")
        text = self.replace_formal_words(text)
        
        print("[3] Menghapus penggunaan kata berlebihan...")
        text = self.remove_overuse_of_certain_words(text)
        
        print("[4] Menambahkan kontraksi...")
        text = self.add_contractions(text)
        
        print("[5] Memvariasikan struktur kalimat...")
        text = self.vary_sentence_structure(text)
        
        print("[6] Menambahkan sentuhan informal...")
        text = self.add_informal_touches(text)
        
        return text


def main():
    """Main program"""
    converter = AItoHumanConverter()
    
    print("\n" + "="*60)
    print("AI TEXT TO HUMAN TEXT CONVERTER")
    print("="*60)
    print("\nOpsi:")
    print("1. Input teks manual")
    print("2. Baca dari file")
    print("3. Exit")
    
    while True:
        choice = input("\nPilih opsi (1/2/3): ").strip()
        
        if choice == '1':
            print("\n[Masukkan teks AI (ketik 'END' di baris baru untuk selesai)]")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            
            ai_text = '\n'.join(lines)
            
            if ai_text.strip():
                print("\n" + "="*60)
                print("PROSES KONVERSI")
                print("="*60)
                
                # Analisis teks original
                print("\n[ANALISIS TEKS ORIGINAL]")
                original_metrics = converter.analyze_humanness(ai_text)
                print_metrics(original_metrics, "Original")
                
                # Konversi
                human_text = converter.convert(ai_text)
                
                # Analisis teks hasil konversi
                print("\n[ANALISIS TEKS HASIL KONVERSI]")
                converted_metrics = converter.analyze_humanness(human_text)
                print_metrics(converted_metrics, "Converted")
                
                # Tampilkan hasil
                print("\n" + "="*60)
                print("HASIL KONVERSI")
                print("="*60)
                print("\n[TEKS ORIGINAL]")
                print(ai_text)
                print("\n[TEKS HASIL KONVERSI]")
                print(human_text)
                print("\n[IMPROVEMENT]")
                print(f"Humanness Score: {original_metrics['humanness_score']} → {converted_metrics['humanness_score']}")
                
                # Tawarkan untuk simpan
                save = input("\nSimpan hasil ke file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Nama file (tanpa .txt): ").strip() or "output"
                    with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
                        f.write("TEKS ORIGINAL:\n")
                        f.write(ai_text)
                        f.write("\n\n" + "="*60 + "\n\n")
                        f.write("TEKS HASIL KONVERSI:\n")
                        f.write(human_text)
                    print(f"✓ Tersimpan ke {filename}.txt")
        
        elif choice == '2':
            filepath = input("Masukkan path file: ").strip()
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    ai_text = f.read()
                
                print("\n" + "="*60)
                print("PROSES KONVERSI")
                print("="*60)
                
                # Analisis teks original
                print("\n[ANALISIS TEKS ORIGINAL]")
                original_metrics = converter.analyze_humanness(ai_text)
                print_metrics(original_metrics, "Original")
                
                # Konversi
                human_text = converter.convert(ai_text)
                
                # Analisis teks hasil konversi
                print("\n[ANALISIS TEKS HASIL KONVERSI]")
                converted_metrics = converter.analyze_humanness(human_text)
                print_metrics(converted_metrics, "Converted")
                
                # Tampilkan hasil
                print("\n" + "="*60)
                print("HASIL KONVERSI")
                print("="*60)
                print(human_text)
                
                # Simpan otomatis
                save = input("\nSimpan hasil ke file? (y/n): ").strip().lower()
                if save == 'y':
                    output_file = filepath.replace('.txt', '_human.txt')
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(human_text)
                    print(f"✓ Tersimpan ke {output_file}")
            
            except FileNotFoundError:
                print(f"✗ File tidak ditemukan: {filepath}")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == '3':
            print("Terima kasih telah menggunakan program ini!")
            break
        
        else:
            print("Opsi tidak valid. Coba lagi.")


def print_metrics(metrics: dict, label: str):
    """Print analisis metrics"""
    print(f"\n{label}:")
    print(f"  Humanness Score: {metrics['humanness_score']}/100")
    print(f"  Rata-rata panjang kalimat: {metrics['avg_sentence_length']:.1f} kata")
    print(f"  Variasi kalimat: {metrics['sentence_variety']:.2f}")
    print(f"  Rasio kata formal: {metrics['formal_words_ratio']:.2%}")
    print(f"  Rasio kata pengisi: {metrics['filler_words_ratio']:.2%}")
    print(f"  Jumlah kontraksi: {metrics['contraction_count']}")


if __name__ == "__main__":
    main()
