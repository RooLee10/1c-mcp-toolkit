# QueryLineageAnalyzer - 1C Native API Component

C++ компонента для загрузки внутрь процесса 1С:Предприятие. Анализирует текст запроса 1С и обогащает `schema` результата `execute_query` полем `sources`.

## Требования

- Windows (x86 или x64)
- CMake 3.16+
- Visual Studio 2022 (MSVC)
- Доступ в интернет на этапе `cmake`, если `include/nlohmann/json.hpp` ещё не закеширован локально

## Сборка

```bash
cd native_components/QueryLineageAnalyzer

# x64
cmake -B build -A x64
cmake --build build --config Release

# x86
cmake -B build_x86 -A Win32
cmake --build build_x86 --config Release

# optional native tests
cmake -B build_tests -A x64 -DQUERY_LINEAGE_BUILD_TESTS=ON
cmake --build build_tests --config Release
ctest --test-dir build_tests -C Release
```

## Установка в обработку

Скопировать DLL нужной разрядности в макет обработки под именем `Template.bin`:

```bash
# x64
cp build/Release/QueryLineageAnalyzer.dll \
  ../../1c/MCPToolkit/MCPToolkit/Templates/QueryLineageAnalyzer/Ext/Template.bin

# x86
cp build_x86/Release/QueryLineageAnalyzer.dll \
  ../../1c/MCPToolkit/MCPToolkit/Templates/QueryLineageAnalyzer/Ext/Template.bin
```

После обновления `Template.bin` нужно пересохранить обработку в конфигураторе 1С.

## API

### Методы

| Method | Alias RU | Params | Return | Description |
|--------|----------|--------|--------|-------------|
| `AnalyzeSources` | `АнализироватьИсточники` | `queryText`, `schemaJson` | `string` | Обогащает `schema` полем `sources` |
| `Version` | `Версия` | - | `string` | Версия компоненты |
