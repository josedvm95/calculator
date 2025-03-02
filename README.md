## Generate executable

`pyinstaller calculator.spec -y`

## Credits

- Calculator icon: <a href="https://www.flaticon.com/free-icons/calculator" title="calculator icons">created by Freepik - Flaticon</a>


## Missing features

- Display history
- Side panel with history when window is wide enough (840p)
- Transform result to scientific notation if it's too big to display. We can use f"{result:15.e}".
- Memory buttons
- Add memory tab to side panel
- Remember last viewed, memory or history, and show that tab when showing side panel
- Save window size on close to reuse it at next open
- Fixed position option
- Left menu with "standard" and "configuration" options
- Add options view
- Animation on opening left menu
- Automatic local language, comma and thousand separator
- Show last operation above current number (probably a label)
- Repeat last operation after pressing equals
- Add buttons: 1/x, x^2, sqrt(x), CE. CE is the same as C, except that when you press it before equals it sets the number to zero leaving the previous operation.
- Add date calculator view
- Resize digits when inputting a big number that would be outside of the window, on the 11th digit and subsequent ones (max digits 16)
- Add angle conversion view
- Add temperature conversion view
- Add volume conversion view
- Add length conversion view
- Add weight conversion view
- Add byte conversion view

## Existing bugs

- After clicking a button the hover color remains