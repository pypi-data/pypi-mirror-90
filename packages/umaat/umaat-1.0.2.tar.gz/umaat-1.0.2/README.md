# umaat-Ultimate Machine-learning Algorithm Accuracy Test
This is a package that houses the functions which can produce accuracy results for each algorithm listed under the categories of Clustering, Regression & Classification based on passing the arguments - independent and dependent variables/features from a given dataset, based on  which the user can choose the best category and algorithm suitable for their  dataset and then implement the machine learning model with the same 
## Development Status:
Under Development (Early release)

### Developed by:

 [Vishal Balaji Sivaraman](https://github.com/TheSocialLion)

### Installation:

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install umaat

### For installation of latest package

```bash
pip install umaat
```
### For installation of a particular version of package

```bash
pip install umaat == version number of package
```

### To import umaat:

```python
import umaat
```
### To use a particular function in umaat:
```python
from umaat import model_accuracy
ma=model_accuracy()
ma.accuracy_test(X,y) 
```

## License:
[MIT](https://choosealicense.com/licenses/mit/)
