# 🚀 CESGA API - Get Started Now

## ⚡ Quick Start (Choose One)

### Option 1: ONE COMMAND (Recommended ⭐)
```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
chmod +x quickstart.sh
./quickstart.sh
```
**Result**: API running at http://localhost:8000 ✅

### Option 2: Manual Setup
```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/init_db_real_proteins.py
python -m uvicorn app.main:app --reload
```

---

## 📍 After Startup

1. **Open Swagger UI**
   ```
   http://localhost:8000/docs
   ```

2. **Test Sample Job**
   ```bash
   curl http://localhost:8000/jobs/sample_ubiquitin/status | jq .
   ```

3. **Check Real Data**
   ```bash
   curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.protein_metadata'
   ```
   Expected: `"uniprot_id": "P0CG47"` (ubiquitin)

---

## 📚 Read First

| Want to... | Read This | Time |
|------------|-----------|------|
| Get running fast | [QUICKSTART.md](QUICKSTART.md) | 5 min |
| Understand what's included | [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | 10 min |
| Use the API | [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) | 10 min |
| Verify it works | [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) | 30 min |
| See all docs | [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | 10 min |

---

## ✅ Checklist

- [ ] Run `./quickstart.sh` successfully
- [ ] API shows "Application startup complete"
- [ ] Can access http://localhost:8000/docs
- [ ] Sample job returns COMPLETED status
- [ ] Real protein detected (ubiquitin = P0CG47)
- [ ] Swagger UI shows 7 endpoints
- [ ] Can submit new job via POST /jobs/submit

---

## 🎯 Core Endpoints (Try These)

### 1. Submit Job
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">test\nMKVLSPADKTNV",
    "fasta_filename": "test.fasta",
    "gpus": 1,
    "cpus": 4,
    "memory_gb": 8
  }'
```

### 2. Check Status
```bash
curl http://localhost:8000/jobs/{job_id}/status
```

### 3. Get Results
```bash
curl http://localhost:8000/jobs/{job_id}/outputs | jq .
```

### 4. List All Jobs
```bash
curl http://localhost:8000/jobs
```

### 5. Health Check
```bash
curl http://localhost:8000/health
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Kill: `lsof -i :8000 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |
| Import errors | Run: `pip install -r requirements.txt` |
| Database locked | Delete `cesga_simulator.db` and re-run init |
| Outputs not ready | Wait ~15 seconds (5s queue + 10s exec), refresh |

---

## 💡 Tips

- **Swagger UI**: Best way to explore - http://localhost:8000/docs
- **Real Proteins**: 6 included (Ubiquitin, Insulin, Hemoglobin, Lysozyme, Amylase, Myoglobin)
- **Sample Jobs**: 4 pre-created jobs available immediately
- **Auto-Detect**: Submit known proteins → automatic real data lookup
- **Customize Timing**: Edit `.env` to change PENDING/RUNNING delays

---

## 📖 Key Files

```
/Users/juditgonzalez/Desktop/API_CESGA/
├── README.md                      ← Start here
├── QUICKSTART.md                  ← Quick setup
├── API_QUICK_REFERENCE.md         ← API examples
├── SPECIFICATIONS.md              ← Full requirements
├── TESTING_REAL_PROTEINS.md       ← Verification tests
├── DOCUMENTATION_INDEX.md         ← All docs
├── quickstart.sh                  ← One-command setup
├── app/                           ← Source code
├── scripts/                       ← Init scripts
└── tests/                         ← Test suite
```

---

## 🎓 Full Learning Path

1. **5 min**: Run `./quickstart.sh`
2. **5 min**: Visit http://localhost:8000/docs
3. **10 min**: Read [QUICKSTART.md](QUICKSTART.md)
4. **10 min**: Read [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md)
5. **10 min**: Try example endpoints
6. **20 min**: Read [SPECIFICATIONS.md](SPECIFICATIONS.md)
7. **30 min**: Run [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) tests
8. **20 min**: Check [ARCHITECTURE.md](ARCHITECTURE.md)

**Total**: ~2 hours to full understanding ✅

---

## 🧬 What You Get

✅ **7 REST Endpoints** - Fully documented  
✅ **Real Proteins** - 6 UniProt sequences  
✅ **Auto-Detection** - Protein identification  
✅ **Biological Data** - Solubility, stability, alerts  
✅ **Structure Files** - PDB, mmCIF, confidence  
✅ **Job Tracking** - State machine with timestamps  
✅ **Accounting** - CPU-hours, GPU-hours, efficiency  
✅ **Logs** - Simulated container output  
✅ **Open API** - Full Swagger documentation  

---

## 🚀 Let's Go!

```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
./quickstart.sh
# Then: open http://localhost:8000/docs
```

**Questions?** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

✨ **Happy coding!** ✨
