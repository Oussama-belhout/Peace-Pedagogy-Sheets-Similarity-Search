## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`, ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### Path Too Long (Windows)

If installation fails with path length errors, enable long paths:
1. Run as Administrator: `gpedit.msc`
2. Navigate to: Local Computer Policy → Computer Configuration → Administrative Templates → System → Filesystem
3. Enable "Enable Win32 long paths"

Or install packages individually:
```bash
pip install owlready2 rdflib numpy pandas scikit-learn
```

## Future Enhancements

- [ ] Web interface for similarity search
- [ ] Natural language query processing
- [ ] Integration with real pedagogical sheets (PDF parsing)
- [ ] Recommendation system for lesson sequences
- [ ] Collaborative filtering based on teacher feedback
- [ ] Export results to various formats (CSV, JSON, PDF)
- [ ] Visualization of lesson similarity networks
- [ ] Multi-language support

## Contributing

To contribute to this project:

1. Add new lessons to `data/` folder
2. Extend ontology classes in `src/ontology_builder.py`
3. Improve similarity metrics in `src/similarity_engine.py`
4. Add tests in `tests/` folder

## License

This project is part of the Peace Pedagogy initiative at UNICA M1.

## References

- Peace Pedagogy (ECP - Éducation à la Culture de Paix)
- OWL 2 Web Ontology Language
- Owlready2 Documentation: https://owlready2.readthedocs.io/
- Protégé: https://protege.stanford.edu/




