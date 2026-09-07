import sys
from temperature_converter.converter import convert_temperature

def main():
    if len(sys.argv) < 4:
        print("Uso: convertidor-temperatura <valor> <origen> <destino>")
        sys.exit(1)
        
    try:
        val = float(sys.argv[1])
        from_unit = sys.argv[2]
        to_unit = sys.argv[3]
        
        result = convert_temperature(val, from_unit, to_unit)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()