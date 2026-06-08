/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Formats a number cleanly into Colombian Pesos layout (e.g. 349000 -> "$349.000 COP")
 */
export const formatCOP = (amount: number): string => {
  const formatted = new Intl.NumberFormat('de-DE', { 
    minimumFractionDigits: 0, 
    maximumFractionDigits: 0 
  }).format(amount);
  return `$${formatted}`;
};
