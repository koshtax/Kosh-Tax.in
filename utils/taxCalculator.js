export function calculateTaxNewRegime(totalGrossSalary) {
    const standardDeduction = 75000;
    const netTaxable = totalGrossSalary - standardDeduction;
    let totalTax = 0;

    if (netTaxable > 700000) {
        if (netTaxable > 400000) totalTax += Math.min(netTaxable - 400000, 400000) * 0.05;
        if (netTaxable > 800000) totalTax += Math.min(netTaxable - 800000, 400000) * 0.10;
        if (netTaxable > 1200000) totalTax += Math.min(netTaxable - 1200000, 400000) * 0.15;
        if (netTaxable > 1600000) totalTax += Math.min(netTaxable - 1600000, 400000) * 0.20;
        if (netTaxable > 2000000) totalTax += Math.min(netTaxable - 2000000, 400000) * 0.25;
        if (netTaxable > 2400000) totalTax += (netTaxable - 2400000) * 0.30;
        
        // 4% Health & Education Cess
        totalTax += totalTax * 0.04;
    } else {
        totalTax = 0; // Section 87A Rebate
    }

    return Math.round(totalTax);
}
