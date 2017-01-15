## Tool to deploy a new CPP Project.

### Automates the annoying task to create a sekeleton for each project

#### Features:

- make format, to run clang-format over all src/ and include/ files

#### TODO: 

- Make install so this can be called from everywhere
- clang-tidy
- Include doxygen
- Include other languages?


#### Example usage: 

./deploy.py . test_project

Going to deplay project: 'test_project' in: /home/datosh/Documents/git/useful_tools/deploy_project
/home/datosh/Documents/git/useful_tools/deploy_project/test_project
```
├── build
├── CMakeLists.txt
├── include
├── src
│   └── main.cpp
└── test
    ├── CMakeLists.txt
    └── test.cpp
```
4 directories, 4 files
